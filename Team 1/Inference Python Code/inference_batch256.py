import sys, argparse

sys.path.append('/tmp/scripts/Anomaly Detection/')  #adjust based on your system's directory
import torch
from torch.utils.data import DataLoader
import boto3
from botocore.exceptions import ClientError
import logging
import os
import fmi
from fmilib.fmi_operations import fmi_communicator
from torch.profiler import profile, ProfilerActivity
import json, platform

def get_cpu_info():
    # CPU Information
    print("CPU Information:")
    print(f"Processor: {platform.processor()}")
    print(f"Architecture: {platform.architecture()}")
    print(f"Machine type: {platform.machine()}")
    print(f"System: {platform.system()}")
    print(f"Platform: {platform.platform()}")
    
    return {
        'processor': platform.processor(),
        'architecture': platform.architecture(),
        'machine': platform.machine(),
        'system': platform.system(),
        'platform': platform.platform()
    }

# RAM Information
def get_ram_info():
    if hasattr(os, 'sysconf'):
        if 'SC_PAGE_SIZE' in os.sysconf_names and 'SC_PHYS_PAGES' in os.sysconf_names:
            page_size = os.sysconf('SC_PAGE_SIZE')  # in bytes
            total_pages = os.sysconf('SC_PHYS_PAGES')
            total_ram = page_size * total_pages  # in bytes
            total_ram_gb = total_ram / (1024 ** 3)  # convert to GB
            print(f"Total memory (GB): {total_ram_gb:.2f}")
            return total_ram_gb
    return None


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def environ_or_required(key, default = None, required=True):

    if default is None:
        return (
            {'default': os.environ.get(key)} if os.environ.get(key)
            else {'required': required}

        )
    else:
        return (
            {'default': os.environ.get(key)} if os.environ.get(key)
            else {'default': default}

        )
#Load Data
def load_data(data_path, device):
    return torch.load(data_path, map_location=device)


#Load Model
def load_model(model_path, device):
    model = torch.load(model_path, map_location=device)
    return model.module.eval()


#Use DataLoader for iterating over batches
def data_loader(data, batch_size):
    return DataLoader(data, batch_size=batch_size, drop_last=True)  #Drop samples out of the batch size


#Iterate over data for predicting the redshift and invoke the evaluation modules
def inference(model, dataloader, plot_to_save_path, device, batch_size, rank, world_size):
    total_time = 0.0  # Initialize total time for execution
    num_batches = 0  # Initialize number of batches
    total_data_bits = 0  # Initialize total data bits processed

    comm = fmi_communicator(world_size, rank)

    comm.hint(fmi.hints.fast)

    comm.barrier()

    with profile(
        activities=[ProfilerActivity.CPU],
        profile_memory=True
    ) as prof:
        for i, data in enumerate(dataloader):
            image = data[0].to(device)  #Image is permuted, cropped and moved to cuda
            magnitude = data[1].to(device)  #magnitude of of channels

            with torch.no_grad():
                _ = model([image, magnitude])  # Model inference

            # Calculate the size of the image and magnitude data in bits
            image_bits = image.element_size() * image.nelement() * 8  # Convert bytes to bits
            magnitude_bits = magnitude.element_size() * magnitude.nelement() * 8  # Convert bytes to bits
            total_data_bits += image_bits + magnitude_bits  # Add data bits for this batch

            num_batches += 1

    num_samples = num_batches * batch_size

    avg = prof.key_averages().total_average()
    # Extract total time and memory usage for CPU and GPU
    total_cpu_memory = avg.cpu_memory_usage / 1e6  # Convert bytes to MB
    # total_gpu_memory = prof.key_averages().total_average().cuda_memory_usage / 1e6  # Convert bytes to MB

    # Extract total CPU and GPU time
    total_time = avg.cpu_time_total / 1e6  # Convert from microseconds to seconds
    # total_gpu_time = prof.key_averages().total_average().cuda_time_total / 1e6  # Convert from microseconds to milliseconds
    avg_time_batch = total_time / num_batches
    
    execution_info = {
        'total_cpu_time (seconds)': total_time,
        'total_cpu_memory (MB)': total_cpu_memory,
        'execution_time (seconds/batch)': avg_time_batch,   # Average execution time per batch
        'num_batches': num_batches,   # Number of batches
        'batch_size': batch_size,   # Batch size
        'device': device,   # Selected device
        'throughput_bps': total_data_bits / total_time,   # Throughput in bits per second (using total_time for all batches)
        'sample_persec': num_samples / total_time,  # Number of samples processed per second
        'cpu_info': get_cpu_info(),
        'ram_info (GB)': get_ram_info(),
        'avg_profile': str(avg),
        'self_cpu_memory (MB)': avg.self_cpu_memory_usage/1e6
    }
    
    with open(plot_to_save_path + 'Results.json', 'w') as json_file:
        json.dump(execution_info, json_file, indent=4)
        
    reduce_res = comm.reduce(total_time, 0, fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.double))

    if rank == 0:
        reduce_info = {
            'total_time': reduce_res
        }

        with open(f'{prj_dir}Plots/ResultsReduce.json', 'w', encoding='utf-8') as redInfo:
            json.dump(reduce_info, redInfo, ensure_ascii=False, indent=4)

        upload_file(
            file_name=f'{prj_dir}Plots/ResultsReduce.json',
            bucket='team-one-s3-cosmic',
            object_name=f'results/{rank}/ResultsReduce.json'
        )

    upload_file(file_name=f'{prj_dir}Plots/Results.json',
                bucket='team-one-s3-cosmic',
                object_name=f'results/{rank}/Results.json')


#This is the engine module for invoking and calling various modules
def engine(args):
    data = load_data(args.data_path, args.device)
    dataloader = data_loader(data, args.batch_size)
    model = load_model(args.model_path, args.device)
    inference(model, dataloader, args.plot_path, device=args.device, batch_size=args.batch_size,
              rank=args.rank, world_size=args.world_size)


# Pathes and other inference hyperparameters can be adjusted below
if __name__ == '__main__':
    prj_dir = '/tmp/scripts/Anomaly Detection/'  #adjust based on your system's directory
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=256)
    parser.add_argument('--data_path', type=str, default=f'{prj_dir}Inference/resized_inference.pt')
    parser.add_argument(
        '--model_path',
        type=str,
        default=f'{prj_dir}Fine_Tune_Model/Mixed_Inception_z_VITAE_Base_Img_Full_New_Full.pt',
    )
    parser.add_argument('--device', type=str, default='cpu')  # To run on GPU, put cuda, and on CPU put cpu

    parser.add_argument('--plot_path', type=str, default=f'{prj_dir}Plots/')

    parser.add_argument('--rank',  type=int, **environ_or_required('RANK', required=False))
    parser.add_argument('--world_size', type=int, **environ_or_required('WORLD_SIZE', required=False))
    args = parser.parse_args()

    engine(args)
