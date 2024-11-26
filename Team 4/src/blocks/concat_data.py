import torch
from torch.utils.data import TensorDataset
import glob


def concat_chunk(pt_files, save_cat_path):
    image_cat = []
    magnitude_cat = []
    redshift_cat = []

    for chunk_path in pt_files:
        # Load each chunk
        chunk = torch.load(chunk_path)

        # Split image, magnitude, and redshift from each chunk
        image_cat.append(chunk[:][0])
        magnitude_cat.append(chunk[:][1])
        redshift_cat.append(chunk[:][2])

    # Concatenate image, magnitude and redshift in separate tensors
    image_cat = torch.cat(image_cat)
    magnitude_cat = torch.cat(magnitude_cat)
    redshift_cat = torch.cat(redshift_cat)

    # Store them as a dataset in save_cat_path
    torch.save(TensorDataset(image_cat, magnitude_cat, redshift_cat), save_cat_path)


# Path to chunks of data
split_path = "Split_Data/"
# Path to save the concatenated data
save_cat_path = "Split_Data/concat_data.pt"
# Read files with .pt format from split_path directory
pt_files = glob.glob(split_path + "*.pt")

# Concatenate chunks and save them in save_cat_path directory
concat_chunk(pt_files, save_cat_path)
