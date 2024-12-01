
# AstroMAE: Redshift Prediction Using a Masked Autoencoder with a Novel Fine-Tuning Architecture

AstroMAE is a novel approach for redshift prediction, designed to address the limitations of traditional machine learning methods that rely heavily on labeled data and feature extraction. Redshift is a key concept in astronomy, referring to the stretching of light from distant galaxies as they move away from us due to the expansion of the universe. By measuring redshift, astronomers can determine the distance and velocity of celestial objects, providing valuable insights into the structure and evolution of the cosmos.

Utilizing a masked autoencoder, AstroMAE pretrains a vision transformer encoder on Sloan Digital Sky Survey (SDSS) images to capture general patterns without the need for labels. This pretrained encoder is then fine-tuned within a specialized architecture for redshift prediction, combining both global and local feature extraction. AstroMAE represents the first application of a masked autoencoder for astronomical data and outperforms other vision transformer and CNN-based models in accuracy, showcasing its potential in advancing our understanding of the cosmos.

### Data Description

This study utilizes data from the Sloan Digital Sky Survey (SDSS), one of the most comprehensive astronomical surveys to date. SDSS is a major multi-spectral imaging and spectroscopic redshift survey, providing detailed data about millions of celestial objects. The dataset used in this experiment is derived from previous work on the AstroMAE project. Specifically, it includes 1,253 images, each with corresponding magnitude values for the five photometric bands (u, g, r, i, z) and redshift targets. Each image has a resolution of 64 × 64 pixels, which are cropped from the center to a size of 32 × 32 pixels to be fed to the model.


<img width="998" alt="image" src="https://github.com/user-attachments/assets/1424e7b6-92bb-4b8d-a62e-b68f695e916e">




  ## AstroMAE Evaluation Metrics

AstroMAE is evaluated using multiple metrics to assess its performance comprehensively. These metrics include Mean Absolute Error (MAE), Mean Square Error (MSE), Bias, Precision, and R² score, offering a complete view of the model's prediction accuracy and reliability, particularly for redshift prediction tasks.

### Scatter Plot: Predicted vs. Spectroscopic Redshift

The scatter plot visualizes the relationship between predicted redshift values (y-axis) and spectroscopic redshift values (x-axis). Each point represents a data sample, with the color indicating point density—warmer colors (yellow to red) denote regions of higher density. The red dashed line represents an ideal scenario (y = x), where predicted redshifts perfectly match spectroscopic values. Closer data points to this line imply better model predictions.

![image](https://github.com/user-attachments/assets/5b51baba-ebad-40d3-89c6-e2e155cca442)

### Metrics Explained

- **Mean Absolute Error (MAE)**: Measures the average magnitude of the errors between predicted and true values, providing insight into prediction accuracy.
- **Mean Square Error (MSE)**: Quantifies the average of squared errors, emphasizing larger deviations to highlight significant prediction errors.
- **Bias**: Measures the average residuals between predicted and true values, indicating any systematic over- or underestimation in predictions.
- **Precision**: Represents the expected scatter of errors, reflecting the consistency of the model's predictions.
- **R² Score**: Evaluates how well the model predicts compared to the mean of true values; a value closer to 1 indicates better predictive performance.

### Additional Metrics

- `total cpu time (second)`: Total time spent on CPU processing during execution, in seconds.
- `total gpu time (second)`: Total time spent on GPU processing during execution, in seconds.
- `execution time per batch (second)`: Average time taken to process each batch, in seconds.
- `cpu memory (MB)`: CPU memory usage during execution, in megabytes.
- `gpu memory (MB)`: GPU memory usage during execution, in megabytes.
- `throughput (bps)`: Data processing rate in bits per second across all batches.
- `batch size`: Number of samples in each batch.
- `number of batches`: The total number of batches processed in the execution.
- `device`: The hardware device (CPU or CUDA) used for execution.

These metrics provide a detailed overview of AstroMAE's performance, emphasizing its effectiveness in redshift prediction tasks.


# AI for Astronomy Inference Step-by-Step Guide

## Overview

This guide provides step-by-step instructions for running inference on the AI for Astronomy project. This process is intended for both Windows and Mac users, though the screenshots and terminal commands shown here are from a Windows computer.

## Prerequisites

- **Python** installed (3.x version recommended).
- Basic understanding of terminal usage.
- Ensure **Git** is installed to clone the repository or download the code.

### Step 1: Clone the Repository

You have two options to get the code:

### Option A: Clone via Terminal

1. Copy the GitHub repository URL: [UVA-MLSys/AI-for-Astronomy](https://github.com/UVA-MLSys/AI-for-Astronomy).
2. Open your terminal and navigate to the directory where you want to save the project.
3. Run the following command:
   ```
   git clone https://github.com/UVA-MLSys/AI-for-Astronomy.git
   ```
4. Follow the prompts to enter your GitHub username, password, or authentication token if required.

### Option B: Download as ZIP

1. From the GitHub page, click on "Download ZIP."
2. Extract the ZIP file by right-clicking on it in your file explorer and selecting "Extract All." Ensure that all files and their structure are maintained.

## Step 2: Set Up the Directory

- Save the extracted or cloned folder to the desired directory from which you will run the Python script.
- If you are using Rivanna or any other computing platform, ensure the folder structure remains intact and accessible by the Python environment or IDE you plan to use.

## Step 3: Update File Paths

1. Navigate to the following directory in your local project folder:
   ```
   ...\AI-for-Astronomy-main\AI-for-Astronomy-main\code\Anomaly Detection\Inference
   ```
2. Locate the `inference.py` file in this directory.

## Step 4: Run the Inference Script

1. Open your terminal and navigate to the directory containing `inference.py`:
   ```sh
   cd ...\AI-for-Astronomy-main\AI-for-Astronomy-main\code\Anomaly Detection\Inference
   ```
2. Run the inference script using the following command:
   ```sh
   python inference.py
   ```
   - The script may take about one minute to complete.
   - If prompted for missing libraries, install them using `pip`. Ensure that the **timm** library version is **0.4.12**.
3.
## Step 5: View Results

1. Once the script completes, navigate to the following directory:
   ```
   ...\AI-for-Astronomy-main\AI-for-Astronomy-main\code\Anomaly Detection\Plots
   ```
2. Open the following files to view the results:
   - **inference.png**: This contains a visual representation of the inference results.
   - **Results.json**: This JSON file contains the detailed numerical results of the inference.

3. Setting the Device

   - To run the script on either GPU or CPU, set the `--device` argument accordingly:

      - For **GPU**: use `'cuda'`
      - For **CPU**: use `'cpu'`

    - The default is set to run on CPU. To change the device, modify the `--device` argument as follows:
    
      ```python
      parser.add_argument('--device', type=str, default='cpu', help="Device to run the model on: 'cuda' for GPU or 'cpu' for CPU")
      ```
### Troubleshooting

- If you encounter issues with missing libraries, ensure you have installed all required packages by using `pip install`. The version of **timm** must be **0.4.12** to avoid compatibility issues.


    #### Setting Up a Python Environment and Installing Packages
    
    Follow these steps to create a Python virtual environment and install the necessary packages (`numpy`, `torch`, `matplotlib`, `scipy`, `sklearn`, `timm`).
    
    ##### Step 1: Create a Virtual Environment
    
    To keep dependencies organized and avoid conflicts, it's recommended to create a virtual environment.
    
    ```sh
    python -m venv myenv
    ```
    
    This command creates a virtual environment named `myenv`.
    
    ##### Step 2: Activate the Virtual Environment
    
    To activate the environment, run:
    
    - On **Windows**:
      ```sh
      myenv\Scripts\activate
      ```
    - On **macOS/Linux**:
      ```sh
      source myenv/bin/activate
      ```
    
    ##### Step 3: Install the Required Packages
    
    Now install all the required packages:
    
    ```sh
    pip install torch==2.2.1 timm==0.4.12
    pip install matplotlib scikit-learn scipy
    pip install numpy==1.23.5
    ```
    
    ##### Deactivating the Environment
      
    ```sh
    deactivate
    ```

### Notes

- Ensure that all directory paths are properly set according to your system's file structure.
- These instructions have been tested on both Windows and Mac systems, with only minor variations.


# Project Folder Structure

```
Anomaly_Detection
├── Fine_Tune_Model
├── Inference
├── Plots
├── blocks
├── Astronomy_Overview.pptx
├── NormalCell.py
├── Plot_Redshift.py
├── README.pdf
```

## Description of Each Folder and File

| Folder/File              | Description                                                                                      |
|--------------------------|--------------------------------------------------------------------------------------------------|
| **Fine_Tune_Model**      | Contains model weights.                                                                         |
| **Inference**            | Code and data required for running inference.                                                   |
| **Plots**                | Generated visualizations, such as plots of model evaluation metrics and analysis results.        |
| **blocks**               | Source code for fine-tuning.                                                                     |
| **Astronomy_Overview.pptx**  | PowerPoint presentation summarizing the astronomy aspects of the project.                      |
| **NormalCell.py**        | Python implementation of standard and customized multi-head self-attention mechanisms.           |
| **Plot_Redshift.py**     | Script for generating visualizations and evaluations related to redshift analysis.               |
| **README.pdf**           | Detailed guide providing step-by-step instructions for running inference.                        |


## Support

Don't hesitate to get in touch with us:

- Amirreza Dolatpour Fathkouhi: aww9gh@virginia.edu
- Kaleigh O'Hara: ear3cg@virginia.edu
