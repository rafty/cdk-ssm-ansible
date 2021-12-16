from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_ec2
from _constructs.ec2_construct import Ec2InstanceConstruct
from _constructs.ssm_endpoint_construct import SsmEndpointConstruct


class Ec2Stack(Stack):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 vpc: aws_ec2.Vpc,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ec2_construct = Ec2InstanceConstruct(
            self,
            'EC2Construct',
            vpc=vpc)

        SsmEndpointConstruct(
            self,
            'SSM Endpoint Construct',
            vpc=vpc
        )
