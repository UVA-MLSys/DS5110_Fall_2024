
### Payload code for running Cosmic AI in Parallel
### Apply the following payload instructions within each execution of the 
### DataParallel-CosmicAI State machine and Step Function. 


## Team 1 Trial - 25mb, File selection 10 files
{
  "bucket": "team-one-cosmic-data",
  "file_limit": "10",
  "batch_size": 512,
  "object_type": "folder",
  "S3_object_name": "Anomaly Detection",
  "script": "/tmp/Anomaly Detection/Inference/inference_data_parallel.py",
  "result_path": "result-partition-25MB/",
  "data_bucket": "team-one-cosmic-data",
  "data_prefix": "25MB"
}


## Team 1 Trial - 25mb, File selection 40 files
{
  "bucket": "team-one-cosmic-data",
  "file_limit": "40",
  "batch_size": 512,
  "object_type": "folder",
  "S3_object_name": "Anomaly Detection",
  "script": "/tmp/Anomaly Detection/Inference/inference_data_parallel.py",
  "result_path": "result-partition-25MB/",
  "data_bucket": "team-one-cosmic-data",
  "data_prefix": "25MB"
}

## Team 1 Trial - 25mb, File selection 80 files
{
  "bucket": "team-one-cosmic-data",
  "file_limit": "80",
  "batch_size": 512,
  "object_type": "folder",
  "S3_object_name": "Anomaly Detection",
  "script": "/tmp/Anomaly Detection/Inference/inference_data_parallel.py",
  "result_path": "result-partition-25MB/",
  "data_bucket": "team-one-cosmic-data",
  "data_prefix": "25MB"
}

## Team 1 Trial - 25mb, File selection 120 files
{
  "bucket": "team-one-cosmic-data",
  "file_limit": "120",
  "batch_size": 512,
  "object_type": "folder",
  "S3_object_name": "Anomaly Detection",
  "script": "/tmp/Anomaly Detection/Inference/inference_data_parallel.py",
  "result_path": "result-partition-25MB/",
  "data_bucket": "team-one-cosmic-data",
  "data_prefix": "25MB"
}


##Payload Template for Reference: 
{
  "bucket": "cosmicai-data",
  "file_limit": "11",
  "batch_size": 512,
  "object_type": "folder",
  "S3_object_name": "Anomaly Detection",
  "script": "/tmp/Anomaly Detection/Inference/inference.py",
  "result_path": "demo/1GB",
  "data_bucket": "cosmicai-data",
  "data_prefix": "100MB"
}