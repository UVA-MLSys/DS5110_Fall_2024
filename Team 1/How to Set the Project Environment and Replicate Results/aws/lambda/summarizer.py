import json
import boto3, logging

def lambda_handler(event, context):
    bucket_name = "cosmicai-data"  # replace with your bucket name
    # prefix = "results" # replace with your folder path within the bucket if needed

    s3_client = boto3.client('s3')
    prefix = event['body'][0]['RESULT_PATH']

    logging.info(f'Combined result will be saved in {prefix}')

    # List all JSON files in the specified bucket and prefix
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    # Check if files exist in the specified location
    if "Contents" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps("Output/No files found in the specified S3 bucket or prefix.")
        }
    
    output_file_key = f"{prefix}/combined_data.json"  # Path for the output file
    all_data = []
    # Loop over each object in the response
    for item in response["Contents"]:
        file_key = item["Key"]
        
        # Only process JSON files
        if file_key.endswith(".json") and file_key != output_file_key:
            # Retrieve the file content
            obj = s3_client.get_object(Bucket=bucket_name, Key=file_key) 
            file_content = obj["Body"].read().decode("utf-8")
            
            # Load JSON data and extend all_data list
            try:
                data = json.loads(file_content)
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
            except json.JSONDecodeError:
                return {
                    "statusCode": 500,
                    "body": json.dumps(f"Error decoding JSON in file {file_key}")
                }

    # Convert concatenated data to JSON string
    concatenated_json = json.dumps(all_data)
    
    # Upload the combined JSON data back to the same folder in S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=output_file_key,
        Body=concatenated_json,
        ContentType="application/json"
    )

    # Return the S3 path of the concatenated JSON file
    return {
        "statusCode": 200,
        "body": json.dumps(f"Combined data uploaded to {output_file_key}")
    }