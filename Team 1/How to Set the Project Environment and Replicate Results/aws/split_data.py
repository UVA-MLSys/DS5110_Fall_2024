from torch.utils.data import TensorDataset
import torch, os, gc
from tqdm import tqdm

#add the data path
load_data_path = '../raw_data/total.pt'
#add the path you want to store chunks
save_data_path = '../raw_data/10MB' # '/'.join(load_data_path.split('/')[:-1])
load_data_name = load_data_path.split('/')[-1].replace('.pt', '')
print(f'Data will be saved in {save_data_path}')
if not os.path.exists(save_data_path):
    os.makedirs(save_data_path, exist_ok=True)
    
# Load the data
data = torch.load(load_data_path, weights_only=False)

# Define the chunk size and data length
data_length = len(data.tensors[0])  # Assuming it's a TensorDataset
#set your desired chunk size
# num_chunks = 60
# chunk_size = (data_length + num_chunks - 1) // num_chunks

chunk_size = 5113//10 # creates exactly 100MB size
num_chunks = (data_length + chunk_size - 1) // chunk_size

print(f'Splitting data of length {data_length} into {num_chunks} chunks of size {chunk_size}')

# Save each chunk separately
for i in tqdm(range(num_chunks)):
    filename = f'{i+1}.pt'
    filepath = os.path.join(save_data_path, filename)
    if os.path.exists(filepath):
        print(f'File {filename} already exists. Skipping...')
        continue
    
    start = i * chunk_size
    end = min((i + 1) * chunk_size, data_length)
    
    # Extracting the chunks correctly from each tensor in the dataset
    chunk_0 = data.tensors[0][start:end].numpy()
    chunk_1 = data.tensors[1][start:end].numpy()
    chunk_2 = data.tensors[2][start:end].numpy()
    
    # Saving the chunks to separate files
    chunk = TensorDataset(torch.tensor(chunk_0), torch.tensor(chunk_1), torch.tensor(chunk_2))
    torch.save(chunk, filepath)
    
    del chunk, chunk_0, chunk_1, chunk_2
    gc.collect()
    # if i == 10:
    #     break