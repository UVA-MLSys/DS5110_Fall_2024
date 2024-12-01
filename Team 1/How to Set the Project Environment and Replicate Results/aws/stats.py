import json, os
import pandas as pd
import numpy as np

# sync aws and local folders
# aws s3 sync s3://cosmicai-data/result-partition-100MB result-partition-100MB

def remove_outliers_and_mean(data, threshold=1.5):
    """
    Removes outliers from the data and calculates the mean of the remaining values.

    Args:
        data (list or array): The data to process.
        threshold (float): The IQR multiplier for outlier detection.

    Returns:
        float: The mean of the data after removing outliers.
    """

    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr

    filtered_data = [x for x in data if lower_bound <= x <= upper_bound]

    return np.mean(filtered_data)

def average_varying_batch_size(batch_sizes, runs):
    all_results = []

    keys = ['total_cpu_time (seconds)', "total_cpu_memory (MB)", "throughput_bps"]
    data_size = '1GB'
    column_name = 'batch_size'

    for batch_size in batch_sizes:
        for run in range(1, runs+1):
            combined_file = f'./result-partition-25MB/{data_size}/Batches/{batch_size}/{run}/combined_data.json'
            with open(combined_file, 'r') as f:
                data = json.load(f)
                
                results = {
                    key: [] for key in keys
                }
                
                for d in data:
                    for key in keys:
                        results[key].append(d[key])
                
                results = pd.DataFrame(results)
                results['run'] = run
                results[column_name] = batch_size
                all_results.append(results)
                
    all_results = pd.concat(all_results)
    all_results['total_bits'] = all_results['throughput_bps'] * all_results['total_cpu_time (seconds)']
    keys.append('total_bits')
    
    # all_results = all_results[['data_size', 'run'] + keys]
    all_results = all_results.groupby([column_name, 'run'])[keys].agg({
        'total_cpu_time (seconds)': remove_outliers_and_mean, 
        "total_cpu_memory (MB)": 'sum', 
        "throughput_bps": 'sum',
        'total_bits': 'sum'
    }).reset_index()
    
    mean = all_results.groupby(column_name)[keys].mean().reset_index()
    mean.insert(1, 'run', 'mean')
    all_results = pd.concat([all_results, mean], axis=0)
    all_results.sort_values([column_name, 'run'], inplace=True)
    
    filename = './results/batch_varying_results.csv'
    all_results.round(2).to_csv(filename, index=False)
    print(f"Results saved to {filename}")

def average_varying_data_size(data_sizes, runs):
    all_results = []

    keys = ['total_cpu_time (seconds)', "total_cpu_memory (MB)", "throughput_bps"]
    partitions = [25, 50, 75, 100] # in MB

    for partition in partitions:
        for data_size in data_sizes:
            for run in range(1, runs+1):
                combined_file = f'./result-partition-{partition}MB/{data_size}/{run}/combined_data.json'
                
                if not os.path.exists(combined_file):
                    print(f'File not found: {combined_file}')
                    continue
                
                with open(combined_file, 'r') as f:
                    data = json.load(f)
                    
                    results = {key: [] for key in keys}
                    for d in data:
                        for key in keys:
                            results[key].append(d[key])
                    
                    results = pd.DataFrame(results)
                    results['partition (MB)'] = partition
                    results['run'] = run
                    
                    if data_size == 'total':
                        results['data (GB)'] = 12.6
                    else: results['data (GB)'] = float(data_size.replace('GB', ''))
                    
                    all_results.append(results)
                
    all_results = pd.concat(all_results)
    all_results['total_bits'] = all_results['throughput_bps'] * all_results['total_cpu_time (seconds)']
    keys.append('total_bits')
    
    # all_results = all_results[['data_size', 'run'] + keys]
    all_results = all_results.groupby(['partition (MB)','data (GB)', 'run'])[keys].agg({
        'total_cpu_time (seconds)': remove_outliers_and_mean, 
        "total_cpu_memory (MB)": 'sum', 
        "throughput_bps": 'sum',
        'total_bits': 'sum'
    }).reset_index()

    mean = all_results.groupby(['partition (MB)','data (GB)'])[keys].mean().reset_index()
    mean.insert(2, 'run', 'mean')
    all_results = pd.concat([all_results, mean], axis=0)
    all_results.sort_values(['partition (MB)', 'data (GB)', 'run'], inplace=True)

    filename = './results/result_stats.csv'
    all_results.round(2).to_csv(filename, index=False)
    print(f'File saved at {filename}')
    
def adjust_throughput_stats():
    result_stats = pd.read_csv('./results/result_stats.csv')
    state_logs = pd.read_csv('./results/state_machine_logs.csv')
    state_logs['run'] = state_logs['run'].astype(str)
    
    state_logs = state_logs[(~state_logs['batch_varying']) & (state_logs['batch_size'] == 512)]
    state_logs.drop(columns=['batch_varying', 'batch_size'], inplace=True)
    
    df = result_stats.merge(state_logs, on=['partition (MB)', 'data (GB)', 'run'])
    
    df['throughput_bps'] = df['total_bits'] / df['inference_duration (s)']
    avg = df.groupby(['partition (MB)', 'data (GB)'])[[
        'total_cpu_time (seconds)', 'total_cpu_memory (MB)',
        'throughput_bps', 'num_worlds','total_duration (s)',
        'inference_duration (s)', 'total_bits'
    ]].mean().reset_index()
    
    avg.insert(2, 'run', 'mean')
    df = pd.concat([df, avg], axis=0)
    df.sort_values(by=['partition (MB)', 'data (GB)', 'run'], inplace=True)
    df.round(2).to_csv('./results/result_stats_adjusted.csv', index=False)
    
def adjust_throughput_batch_varying():
    result_stats = pd.read_csv('./results/batch_varying_results.csv')
    state_logs = pd.read_csv('./results/state_machine_logs.csv')
    state_logs['run'] = state_logs['run'].astype(str)
    
    state_logs = state_logs[state_logs['batch_varying']& (state_logs['data (GB)'] == 1)]
    state_logs.drop(columns=['batch_varying', 'partition (MB)', 'data (GB)'], inplace=True)
    
    df = result_stats.merge(state_logs, on=['batch_size', 'run'])
    
    df['throughput_bps'] = df['total_bits'] / df['inference_duration (s)']
    avg = df.groupby('batch_size')[[
        'total_cpu_time (seconds)', 'total_cpu_memory (MB)',
        'throughput_bps', 'num_worlds','total_duration (s)',
        'inference_duration (s)', 'total_bits'
    ]].mean().reset_index()
    
    avg.insert(1, 'run', 'mean')
    df = pd.concat([df, avg], axis=0)
    df.sort_values(by=['batch_size', 'run'], inplace=True)
    df.round(2).to_csv('./results/batch_varying_adjusted.csv', index=False)

if __name__ == '__main__':
    partitions = [25, 50, 75, 100] # in MB
    data_sizes = ['1GB', '2GB', '4GB', '6GB', '8GB', '10GB', 'total']
    runs = 3
    batch_sizes = [32, 64, 128, 256, 512]
    
    average_varying_batch_size(batch_sizes, runs)
    adjust_throughput_batch_varying()
    
    average_varying_data_size(data_sizes, runs)
    adjust_throughput_stats()
    