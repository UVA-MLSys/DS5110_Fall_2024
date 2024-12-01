import boto3
from datetime import datetime, timedelta
import pytz

def get_lambda_logs(function_name, start_time, end_time):
    """
    Collects log events for a Lambda function within a specified time period.

    :param function_name: Name of the Lambda function
    :param start_time: Start time as a datetime object
    :param end_time: End time as a datetime object
    """
    # Initialize boto3 client for CloudWatch Logs
    logs_client = boto3.client('logs')

    # The log group for Lambda functions is in the format '/aws/lambda/<function_name>'
    log_group_name = f"/aws/lambda/{function_name}"

    # Convert datetime to timestamp in milliseconds
    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    try:
        print(f"Fetching logs for Lambda function '{function_name}' from {start_time} to {end_time}...\n")
        
        # Get the log streams for the Lambda function
        log_streams = logs_client.describe_log_streams(
            logGroupName=log_group_name,
            orderBy="LastEventTime",
            descending=True,
            limit=5
        )
        
        print(f'Found {len(log_streams["logStreams"])} log streams for Lambda function "{function_name}".')

        # Iterate through log streams
        for stream in log_streams['logStreams']:
            log_stream_name = stream['logStreamName']

            # Get log events from the log stream
            events = logs_client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                # startTime=start_time_ms,
                # endTime=end_time_ms,
                startFromHead=True
            )

            print(f"Log stream: {log_stream_name}, events: {len(events['events'])}")

            # Print events
            for event in events['events']:
                event_time = datetime.fromtimestamp(event['timestamp'] / 1000, tz=pytz.utc)
                print(f"{event_time} - {event['message'].strip()}")
            if len(events['events']) > 1:
                break
            
            print("\n")

    except logs_client.exceptions.ResourceNotFoundException:
        print(f"Log group {log_group_name} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Lambda function name
    lambda_function_name = "cosmic-executor"

    # Define the time period (last 24 hours in this example)
    end_time = datetime.now(pytz.utc)- timedelta(days=2)
    start_time = end_time - timedelta(days=3)

    # Get logs
    get_lambda_logs(lambda_function_name, start_time, end_time)
