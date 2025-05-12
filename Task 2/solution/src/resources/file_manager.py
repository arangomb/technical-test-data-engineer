import boto3

from solution.src.config.env import ENERGY_BUCKET_NAME

class FileManagerResource():

    def __init__(self) -> None:
        self.client = boto3.client("s3")
        self.bucket_name = ENERGY_BUCKET_NAME


    def copy_object(self, origin_key:str, final_key:str, origin_bucket_name:str) -> None:

        self.client.copy_object(
            Bucket=self.bucket_name,
            CopySource={'Bucket': origin_bucket_name, 'Key': origin_key},
            Key=final_key
        )
    
    def download_object(self, key:str, download_path:str) -> None:

        self.client.download_file(
            Bucket=self.bucket_name,
            Key=key,
            Filename=download_path
        )

    def list_objects(self, bucket: str, prefix: str) -> dict:

        return self.client.list_objects_v2(Bucket=bucket, Prefix=prefix)