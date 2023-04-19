import os

import boto3

from emr_cli.deployments.emr_serverless import DeploymentPackage
from emr_cli.utils import console_log, parse_bucket_uri


class SimpleProject(DeploymentPackage):

    def __init__(self, profile: str = None):
        super().__init__(profile)

        self.s3_client = self.aws_session.client("s3")

    """
    A simple project only has a single entry point file.
    This can be a pyspark file or packaged jar file.
    """

    def build(self):
        pass

    def deploy(self, s3_code_uri: str) -> str:
        """
        Copies local code to S3 and returns the path to the uploaded entrypoint
        """
        
        bucket, prefix = parse_bucket_uri(s3_code_uri)
        filename = os.path.basename(self.entry_point_path)

        console_log(f"Deploying {filename} to {s3_code_uri}")

        self.s3_client.upload_file(self.entry_point_path, bucket, f"{prefix}/{filename}")

        return f"s3://{bucket}/{prefix}/{filename}"
