import boto3

class AWSConnectionManager:
    def __init__(self, config=None):
        self.config = config

    def connect_to_s3(self, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
        try:
            aws_access_key_id = aws_access_key_id or self.config["aws"]["access_key_id"]
            aws_secret_access_key = aws_secret_access_key or self.config["aws"]["secret_access_key"]
            region_name = region_name or self.config["aws"]["region_name"]
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
            )
            print("Successfully connected to AWS S3.")
            return s3_client
        except Exception as e:
            raise ConnectionError(f"Failed to connect to AWS S3: {e}")