import boto3
from dotenv import dotenv_values

# should probably set as a fixture :TODO
config :dict = dotenv_values(".env")


def test_can_find_config() -> None:
    """is the config valid"""
    assert len(config) > 1, "the config appears empty"

def test_s3_connection() -> None:
    """Validate the S3 connection to current credentials"""
    session = boto3.Session(aws_access_key_id=config["aws_access_key_id"],
                            aws_secret_access_key=config["aws_secret_access_key"],
                            region_name=config["region"])

    s3 = session.client('s3')

    d = s3.list_buckets()

    # current buckets
    b = [n["Name"] for n in d["Buckets"]]

    assert 'fmi-lambda-demo' in b, "missing the lambda demo" 
    assert 'team4-cosmicai' in b, "missing our team4 cosmicai S3 connection" 

