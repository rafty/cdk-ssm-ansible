from constructs import Construct
from aws_cdk import aws_s3
from aws_cdk import aws_s3_deployment


class S3DeployConstruct(Construct):
    def __init__(self,
                 scope: Construct,
                 id: str,
                 bucket_name: str,
                 key_prefix: str,
                 source_asset: str,
                 ) -> None:
        super().__init__(scope, id)

        self._key_prefix = key_prefix
        self._bucket_name = bucket_name

        # ----------------------------------------------------
        # S3 Bucket
        # ----------------------------------------------------
        self._bucket = aws_s3.Bucket(self, 'S3BucketConstruct', bucket_name=bucket_name)

        # ----------------------------------------------------
        # S3 ansible playbook Upload
        # ----------------------------------------------------
        aws_s3_deployment.BucketDeployment(
            self,
            'AnsiblePlayBookUpload',
            sources=[aws_s3_deployment.Source.asset(source_asset)],
            destination_bucket=self._bucket,
            destination_key_prefix=key_prefix
        )

    @property
    def bucket(self):
        return self._bucket

    @property
    def key_prefix(self):
        return self._key_prefix

