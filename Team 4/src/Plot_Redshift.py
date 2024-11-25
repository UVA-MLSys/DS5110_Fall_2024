import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.stats import gaussian_kde

def plot_density(x, y, save_plot_path):
    x = np.array(x)
    y = np.array(y)
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)
    # Sort the points by density, so that the densest points are plotted last
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]
    fig, ax = plt.subplots()

    scatter = ax.scatter(x, y, c=z, s=1, cmap='inferno')

    # Adding a dashed line
    ax.plot([min(min(x), min(y)), max(max(x), max(y))], [min(min(x), min(y)), max(max(x), max(y))], '--', color='red') # Change coordinates as needed

    plt.xlim(min(min(x), min(y)), max(max(x), max(y)))
    plt.ylim(min(min(x), min(y)), max(max(x), max(y)))
    
    plt.xlabel('spectroscopic z')
    plt.ylabel('predicted z')
    plt.grid(True)
    plt.colorbar(scatter, ax=ax)
    
    plt.savefig(save_plot_path + '/inference.png')




def err_calculate(prediction, z, execution_info, save_path):
    
    def r2_score(y_true, y_pred):
        # Calculate the residual sum of squares
        ss_res = np.sum((y_true - y_pred) ** 2)

        # Calculate the total sum of squares
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)

        # Calculate R^2 score
        r2 = 1 - (ss_res / ss_tot)

        return r2
 
    prediction = np.array(prediction)
    z = np.array(z)
    
    #MAE
    mae = np.sum(abs(prediction - z)) / z.shape[0]
    
    #MSE
    mse = np.sum((prediction - z)**2) / z.shape[0]    
    
    #Delta
    deltaz = (prediction - z) / (1 + z)
    
    #Bias
    bias = np.sum(deltaz) / z.shape[0]
    
    #Precision
    nmad = 1.48 * np.median(abs(deltaz - np.median(deltaz)))
    
    #R^2 score
    r2 = r2_score(z, prediction)
     
    #All errors are stored in a json and saved in  save_path directory
    errs = {
    'total cpu time (second)': execution_info['total_cpu_time'],
    'total gpu time (second)': execution_info['total_gpu_time'],
    'execution time per batch (second)': execution_info['execution_time_per_batch'],
    'cpu memory (MB)': execution_info['total_cpu_memory'],
    'gpu memory (MB)': execution_info['total_gpu_memory'],
    'throughput(bps)': execution_info['throughput_bps'],
    'batch size': execution_info['batch_size'],
    'number of batches': execution_info['num_batches'],
    'device': execution_info['device'],
    'MAE': mae,
    'MSE': mse,
    'Bias': bias,
    'Precision': nmad,
    'R2': r2
    }
    
    with open(save_path + 'Results.json', 'w') as file:
        json.dump(errs, file, indent=5)
