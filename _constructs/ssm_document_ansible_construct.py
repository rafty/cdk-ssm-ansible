import json
from constructs import Construct
from aws_cdk import aws_ssm
from aws_cdk import aws_s3
from _constructs.s3_deployment_construct import S3DeployConstruct


class SsmAssociationConstruct(Construct):
    def __init__(self,
                 scope: Construct,
                 id: str,
                 ) -> None:
        super().__init__(scope, id)

        # -------------------------------------------------
        # Ansible Play Book Bucket
        # -------------------------------------------------
        ansible_construct = S3DeployConstruct(
            self,
            'AnsiblePlaybookBucket',
            bucket_name='ygt-ansible-playbook',
            key_prefix='apache',
            source_asset='./ansible/apache'  # local yaml path
        )

        # -------------------------------------------------
        # Association Log
        # -------------------------------------------------
        ssm_logs = aws_s3.Bucket(self, 'AssociationLogBucket', bucket_name='ygt-ssm-logs')
        output_location = aws_ssm.CfnAssociation.InstanceAssociationOutputLocationProperty(
            s3_location=aws_ssm.CfnAssociation.S3OutputLocationProperty(
                output_s3_bucket_name=ssm_logs.bucket_name,
                output_s3_key_prefix='ansible/'
            )
        )

        ssm_ansible = aws_ssm.CfnAssociation(
            self,
            'AnsibleSSMAssociation',
            name='AWS-ApplyAnsiblePlaybooks',
            association_name='AnsibleAssociation',
            # parameters={
            #     'SourceType': ['S3'],
            #     'SourceInfo': [json.dumps({
            #         'path': "https://s3.amazonaws.com/DOC-EXAMPLE-BUCKET/"
            #     })],
            #     'InstallDependencies': ['True'],
            #     'PlaybookFile': ['ansible/playbook.yml'],
            #     'ExtraVariables': ['SSM=True'],
            #     'Check': ['False'],
            #     'Verbose': ['-v']
            # },
            # apply_only_at_cron_interval=False,
            # schedule_expression='rate(30 minutes)',
            targets=[
                aws_ssm.CfnAssociation.TargetProperty(
                    key='tag:ansible',
                    values=[
                        'play'
                    ]
                )
            ],
            wait_for_success_timeout_seconds=120,
            output_location=output_location
        )

        ssm_ansible.add_override('Parameters.SourceType', ['S3'])
        ssm_ansible.add_override('Parameters.SourceInfo.0', [
            json.dumps(
                {
                    'path': f'{ansible_construct.bucket.bucket_website_url}//'
                }
            )
        ])
        ssm_ansible.add_override('Parameters.InstallDependencies', ['True'])
        ssm_ansible.add_override('Parameters.PlaybookFile', ['ansible/playbook.yml'])
        ssm_ansible.add_override('Parameters.ExtraVariables', ['SSM=True'])
        ssm_ansible.add_override('Parameters.Check', ['False'])
        ssm_ansible.add_override('Parameters.Verbose', ['-v'])
