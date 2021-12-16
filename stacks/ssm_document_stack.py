import yaml
from aws_cdk import Stack
from constructs import Construct
from _constructs.ssm_document_ansible_construct import SsmAnsibleAssociationConstruct
# from aws_cdk import aws_ssm
# from aws_cdk import CfnTag


class SsmDocumentStack(Stack):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 # ssm_document_name: str,  # RunAnsiblePlayBook
                 # ssm_document_yaml: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        SsmAnsibleAssociationConstruct(
            self,
            'AnsibleAssociationConstruct',
        )
