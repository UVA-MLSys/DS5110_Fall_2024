import json, boto3
import os, logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')

def get_ith_filename(i):
    return f'{i+1}.pt'

def get_file_list(bucket, prefix):
    response = s3_client.list_objects_v2(
        Bucket=bucket, Prefix=prefix
    )
    # Check if files exist in the specified location
    if "Contents" not in response:
        logger.error("Inference: No files found in the specified S3 bucket or prefix.")
        return []

    filenames = []
    # Loop over each object in the response
    for item in response["Contents"]:
        file_key = item["Key"]
        
        # Only process pt files
        if file_key.endswith(".pt"):
            filenames.append(file_key)

    # consistency checking
    for i in range(len(filenames)):
        filename = get_ith_filename(i)
        if filename in filenames: continue
        logging.error(f'{filename} is missing.')
    
    return filenames

def ceil(a, b): 
    return (a+b-1) // b
    
def lambda_handler(event, context): 
    bucket = event["bucket"]
    object_type = event["object_type"]
    
    script = event["script"]
    S3_object_name = event["S3_object_name"]
    result_path = event['result_path']
    file_limit = int(event['file_limit'])
    batch_size = int(event['batch_size'])

    # if you want one task to handle multiple files
    if "world_size" in event:
        world_size = int(event["world_size"])
    else: 
        world_size = file_limit
    
    # partitioned data are physically located here
    data_bucket = event['data_bucket'] # 'cosmicai-data'
    data_bucket_prefix = event['data_prefix'] # ''
    filenames = get_file_list(bucket=data_bucket, prefix=data_bucket_prefix)
    filenames = filenames[:file_limit]
    # logging.info(f'Files {filenames}')

    result = []
    # dict to store which rank will use which data partition
    data_map = {}
    start_index = 0
    total_files = len(filenames)
    for rank in range(0, int(world_size)):
        if rank < total_files: 
            # num files left / num of worlds left
            step_size = ceil(total_files - start_index, world_size - rank)
            # logging.info(f'Rank {rank}, start {start_index}, step size {step_size}.')

            if step_size == 1:
                data_path = filenames[start_index]
            else: 
                data_path = filenames[start_index:start_index+step_size]
            start_index += step_size

        else: data_path = None
        data_map[rank] = data_path

        payload = {
            "S3_BUCKET": bucket,
            "S3_OBJECT_NAME": S3_object_name,
            "SCRIPT": script,
            "S3_OBJECT_TYPE": object_type,
            "WORLD_SIZE": str(world_size),
            "RANK": str(rank),
            "DATA_BUCKET": data_bucket,
            "DATA_PREFIX": data_bucket_prefix,
            "DATA_PATH": data_path,
            "RESULT_PATH": result_path,
            "BATCH_SIZE": batch_size
        }
        result.append(payload)

    event['data_map'] = data_map
    # used by the container to know world settings
    s3_client.put_object(
        Bucket=bucket,Key='payload.json',
        Body=json.dumps(event, indent = 4),
        ContentType="application/json"
    )
    
    return {
        'statusCode': 404 if filenames is None else 200,
        'body': result
    }