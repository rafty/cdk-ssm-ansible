from aws_cdk import Stack
from constructs import Construct
from _constructs.vpc_construct import VpcConstruct


class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc_construct = VpcConstruct(self, 'VpcConstruct')

    @property
    def vpc(self):
        return self.vpc_construct.vpc
