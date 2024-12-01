import sys, argparse, json
from torch.profiler import profile, record_function, ProfilerActivity
# sys.path.append('/scratch/aww9gh/Cosmic_Cloud/AI-for-Astronomy/code/Anomaly Detection/') #adjust based on your system's directory
sys.path.append('..') #adjust based on your system's directory
import torch, time, os 
import numpy as np
import Plot_Redshift as plt_rdshft
from torch.utils.data import DataLoader
from blocks.model_vit_inception import ViT_Astro 

#Load Data
def load_data(data_path, device):
    return torch.load(data_path, map_location = device)

#Load Model
def load_model(model_path, device):
    model = torch.load(model_path, map_location = device)
    return model.module.eval()

#Use DataLoader for iterating over batches
def data_loader(data, batch_size):
    return DataLoader(data, batch_size = batch_size, drop_last = False)   #Drop samples out of the batch size


# Define the inference function with profiling for both CPU and GPU memory usage
def inference(model, dataloader, real_redshift, save_path, device, batch_size):
    redshift_analysis = []
    total_time = 0.0  # Initialize total time for execution
    num_batches = 0   # Initialize number of batches
    total_data_bits = 0  # Initialize total data bits processed

    # Initialize the profiler to track both CPU and GPU activities and memory usage
    with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
                 profile_memory=True,
                 record_shapes=True) as prof:

        for i, data in enumerate(dataloader):
            with torch.no_grad():
                image = data[0].to(device)  # Image to device
                magnitude = data[1].to(device)  # Magnitude to device

                with record_function("model_inference"):
                    predict_redshift = model([image, magnitude])  # Model inference

                # Append the redshift prediction to analysis list
                redshift_analysis.append(predict_redshift.view(-1, 1))
                num_batches += 1
                
                # Calculate data size for this batch
                image_bits = image.element_size() * image.nelement() * 8  # Convert bytes to bits
                magnitude_bits = magnitude.element_size() * magnitude.nelement() * 8  # Convert bytes to bits
                total_data_bits += image_bits + magnitude_bits  # Add data bits for this batch

    num_samples = len(real_redshift)
    redshift_analysis = torch.cat(redshift_analysis, dim=0)
    redshift_analysis = redshift_analysis.cpu().detach().numpy().reshape(num_samples,) 
    
    # Extract total time and memory usage for CPU and GPU
    total_cpu_memory = prof.key_averages().total_average().cpu_memory_usage / 1e6  # Convert bytes to MB
    total_gpu_memory = prof.key_averages().total_average().cuda_memory_usage / 1e6  # Convert bytes to MB

    # Extract total CPU and GPU time
    total_cpu_time = prof.key_averages().total_average().cpu_time_total / 1e6  # Convert from microseconds to seconds
    total_gpu_time = prof.key_averages().total_average().cuda_time_total / 1e6  # Convert from microseconds to seconds

    
    total_time = max(total_cpu_time, total_gpu_time)
  
    avg_time_batch = total_time / num_batches
    
    execution_info = {
            'total_cpu_time': total_cpu_time,
            'total_gpu_time': total_gpu_time,
            'total_cpu_memory': total_cpu_memory, 
            'total_gpu_memory': total_gpu_memory,
            'execution_time_per_batch': avg_time_batch,   # Average execution time per batch
            'num_batches': num_batches,   # Number of batches
            'batch_size': batch_size,   # Batch size
            'device': device,   # Selected device
            'throughput_bps': total_data_bits / total_time,   # Throughput in bits per second (using total_time for all batches)
        }
    # Invoke the evaluation metrics
    plt_rdshft.err_calculate(redshift_analysis, real_redshift, execution_info, save_path)  
    plt_rdshft.plot_density(redshift_analysis, real_redshift, save_path)
    

#This is the engine module for invoking and calling various modules
def engine(args):
    data = load_data(args.data_path, args.device)
    dataloader = data_loader(data, args.batch_size)
    model = load_model(args.model_path, args.device)
    inference(model, dataloader, data[:][2].to('cpu'), args.save_path, device = args.device, batch_size = args.batch_size)

    
# Pathes and other inference hyperparameters can be adjusted below
if __name__ == '__main__':
    prj_dir = '../' #adjust based on your system's directory
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=512)
    parser.add_argument('--data_path', type = str, default = 'resized_inference.pt')
    parser.add_argument('--model_path', type = str, default  = prj_dir + 'Fine_Tune_Model/Mixed_Inception_z_VITAE_Base_Img_Full_New_Full.pt')
    parser.add_argument('--device', type = str, default = 'cpu')    # To run on GPU, put cuda, and on CPU put cpu

    parser.add_argument('--save_path', type = str, default = prj_dir + 'Plots/')
    args = parser.parse_args()
    engine(args)
