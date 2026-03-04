import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import logging
import pathlib

class S3Sync:
    def __init__(self):
        self.endpoint = os.getenv("S3_ENDPOINT")
        self.bucket = os.getenv("S3_BUCKET")
        self.prefix = os.getenv("S3_PREFIX", "chroma")
        access = os.getenv("AWS_ACCESS_KEY_ID")
        secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_REGION", "ru-central1")
        config = Config(signature_version="s3v4", region_name=region)
        params = {"aws_access_key_id": access, "aws_secret_access_key": secret, "config": config}
        if self.endpoint:
            params["endpoint_url"] = self.endpoint
        self.s3 = boto3.client("s3", **{k: v for k, v in params.items() if v})

    def _key_for(self, local_path: str, local_root: str):
        rel = pathlib.Path(local_path).relative_to(local_root).as_posix()
        return f"{self.prefix.rstrip('/')}/{rel}"

    def download_dir(self, local_dir: str):
        os.makedirs(local_dir, exist_ok=True)
        paginator = self.s3.get_paginator("list_objects_v2")
        try:
            for page in paginator.paginate(Bucket=self.bucket, Prefix=self.prefix):
                for obj in page.get("Contents", []) or []:
                    key = obj["Key"]
                    rel = key[len(self.prefix.rstrip("/"))+1:] if key.startswith(self.prefix.rstrip("/")) else key
                    if not rel:
                        continue
                    dest = os.path.join(local_dir, rel)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    try:
                        self.s3.download_file(self.bucket, key, dest)
                    except ClientError:
                        logging.exception("download failed %s", key)
        except ClientError:
            logging.exception("s3 list/download failed")

    def upload_dir(self, local_dir: str):
        if not os.path.exists(local_dir):
            return
        for root, _, files in os.walk(local_dir):
            for f in files:
                local_path = os.path.join(root, f)
                key = self._key_for(local_path, local_dir)
                try:
                    self.s3.upload_file(local_path, self.bucket, key)
                except ClientError:
                    logging.exception("upload failed %s", local_path)
