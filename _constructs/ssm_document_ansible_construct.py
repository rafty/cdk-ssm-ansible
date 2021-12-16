import json
from constructs import Construct
from aws_cdk import aws_ssm
from aws_cdk import aws_s3
from _constructs.s3_deployment_construct import S3DeployConstruct


class SsmAnsibleAssociationConstruct(Construct):
    def __init__(self,
                 scope: Construct,
                 id: str,
                 ) -> None:
        super().__init__(scope, id)

        # -------------------------------------------------
        # Upload Ansible Play Book to S3
        # -------------------------------------------------
        ansible_construct = S3DeployConstruct(
            self,
            'AnsiblePlaybookBucket',
            bucket_name='ygt-ansible-playbook',
            key_prefix='apache',
            source_asset='./ansible/apache'  # local yaml path
        )

        # -------------------------------------------------
        # SSM State Manager Log
        # -------------------------------------------------
        ssm_logs = aws_s3.Bucket(self, 'AssociationLogBucket', bucket_name='ygt-ssm-logs')
        s3_location = aws_ssm.CfnAssociation.S3OutputLocationProperty(
            output_s3_bucket_name=ssm_logs.bucket_name,
            output_s3_key_prefix='ansible_log/'
        )
        output_location = aws_ssm.CfnAssociation.InstanceAssociationOutputLocationProperty(
            s3_location=s3_location
        )
        # ------------------------------------------------------------------
        # Tag(key=ansible, value=play)のインスタンスすべてをターゲットにする。
        # valueを複数指定することも可能。
        # key='InstanceIds', value=[EC2Instance1Id, EC2Instance2Id]とすればInstanceIdを指定することも可能
        # ------------------------------------------------------------------
        target_ec2_instances = aws_ssm.CfnAssociation.TargetProperty(
            key='tag:ansible',
            values=[
                'play'
            ]
        )
        ssm_document_parameters = {
            'SourceType': ['S3'],
            'SourceInfo': [
                json.dumps(
                    {
                        "path": "https://ygt-ansible-playbook.s3.ap-northeast-1.amazonaws.com/apache/apache.yml"
                    }
                )
            ],
            'InstallDependencies': ['True'],
            'PlaybookFile': ['apache.yml'],
            # 'ExtraVariables': ['SSM=True'],
            # 'Check': ['False'],
            # 'Verbose': ['-v']
        }
        ssm_ansible = aws_ssm.CfnAssociation(
            self,
            'AnsibleSSMAssociation',
            name='AWS-ApplyAnsiblePlaybooks',
            association_name='AnsibleAssociation',
            targets=[target_ec2_instances],
            parameters=ssm_document_parameters,
            wait_for_success_timeout_seconds=300,
            output_location=output_location
        )

        # - Parametersを以下に置き換えることは可能か？
        # ssm_ansible.add_override('Parameters.SourceType', ['S3'])
        # ssm_ansible.add_override('Parameters.SourceInfo.0', [
        #     json.dumps(
        #         {
        #             'path': f'{ansible_construct.bucket.bucket_website_url}//'
        #         }
        #     )
        # ])
        # ssm_ansible.add_override('Parameters.InstallDependencies', ['True'])
        # ssm_ansible.add_override('Parameters.PlaybookFile', ['ansible/playbook.yml'])
        # ssm_ansible.add_override('Parameters.ExtraVariables', ['SSM=True'])
        # ssm_ansible.add_override('Parameters.Check', ['False'])
        # ssm_ansible.add_override('Parameters.Verbose', ['-v'])
