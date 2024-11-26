from typing import Self

from dotenv import dotenv_values
import torch
from torch.profiler import profile, record_function, ProfilerActivity
from torch.utils.data import DataLoader

import Plot_Redshift as plt_rdshft

config: dict = dotenv_values(".env")

class AstronomyAI:
    def __init__(self, batch_size=512, device="cpu") -> Self:
        self.batch_size = batch_size
        self.data = torch.load(config["data"])  # can change when testing new data 'resized_inference.pt'
        self.device = device
        self.model_path = torch.load(config["model_path"]).model.module.eval()  # 'Fine_Tune_Model/Mixed_Inception_z_VITAE_Base_Img_Full_New_Full.pt'
        self.save_path = "Plots/"
        self.real_redshift = self.data[:][2].to("cpu")

        if self.device not in ["cpu", "gpu"]:
            raise "device can only be cpu or gpu"

    def set_data(self, new_data_path:str) -> Self:
        self.data = torch.load(new_data_path)

    def run_inference(self, save_plot = False) -> dict:
        redshift_analysis = []
        total_time = 0.0  
        num_batches = 0 
        total_data_bits = 0 
        dataloader = DataLoader(self.data, batch_size = self.batch_size, drop_last = False)
       

        # Initialize the profiler to track both CPU and GPU activities and memory usage
        with profile(
            activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
            profile_memory=True,
            record_shapes=True) as prof:

            for _, data in enumerate(dataloader):
                with torch.no_grad():
                    image = data[0].to(self.device)  # Image to device
                    magnitude = data[1].to(self.device)  # Magnitude to device

                    with record_function("model_inference"):
                        predict_redshift = self.model([image, magnitude])  # Model inference

                    # Append the redshift prediction to analysis list
                    redshift_analysis.append(predict_redshift.view(-1, 1))
                    num_batches += 1

                    # Calculate data size for this batch
                    image_bits = (
                        image.element_size() * image.nelement() * 8
                    )  # bytes -> bits
                    magnitude_bits = (
                        magnitude.element_size() * magnitude.nelement() * 8
                    )  # bytes -> bits
                    total_data_bits += (
                        image_bits + magnitude_bits
                    ) 

        num_samples = len(self.real_redshift)
        redshift_analysis = torch.cat(redshift_analysis, dim=0)
        redshift_analysis = (
            redshift_analysis.cpu() # TODO: what if its gpu?
            .detach()
            .numpy()
            .reshape(
                num_samples,
            )
        )

        # Extract total time and memory usage for CPU and GPU
        total_cpu_memory = (
            prof.key_averages().total_average().cpu_memory_usage / 1e6
        )  # bytes -> MB
        total_gpu_memory = (
            prof.key_averages().total_average().cuda_memory_usage / 1e6
        )  # bytes -> MB

        # Extract total CPU and GPU time
        total_cpu_time = (
            prof.key_averages().total_average().cpu_time_total / 1e6
        )  # Convert from microseconds to seconds
        total_gpu_time = (
            prof.key_averages().total_average().cuda_time_total / 1e6
        )  # Convert from microseconds to seconds

        total_time = max(total_cpu_time, total_gpu_time)

        avg_time_batch = total_time / num_batches

        execution_info = {
            "total_cpu_time": total_cpu_time,
            "total_gpu_time": total_gpu_time,
            "total_cpu_memory": total_cpu_memory,
            "total_gpu_memory": total_gpu_memory,
            "execution_time_per_batch": avg_time_batch,  # Average execution time per batch
            "num_batches": num_batches,  # Number of batches
            "batch_size": self.batch_size,  # Batch size
            "device": self.device,  # Selected device
            "throughput_bps": total_data_bits
            / total_time,  # Throughput in bits per second (using total_time for all batches)
        }
        
        if save_plot:
            # Invoke the evaluation metrics
            plt_rdshft.err_calculate(redshift_analysis, self.real_redshift, execution_info, self.save_path)
            plt_rdshft.plot_density(redshift_analysis, self.real_redshift, self.save_path)

        return execution_info


