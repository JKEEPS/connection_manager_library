import boto3
from typing import Optional, Dict

class AWSConnectionManager:
    """
    Manages connections to AWS services like S3.
    """
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialise AWS connection manager.

        :param config: A dictionary containing AWS credentials.
        """
        self.config: Optional[Dict] = config

    def connect_to_s3(self, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, region_name: Optional[str] = None) -> boto3.client:
        """
        Connect to AWS S3.

        :param aws_access_key_id: AWS access key ID.
        :param aws_secret_access_key: AWS secret access key.
        :param region_name: AWS region name.
        :return: Boto3 S3 client object.
        """
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
