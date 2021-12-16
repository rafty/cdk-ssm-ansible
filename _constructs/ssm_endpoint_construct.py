from constructs import Construct
from aws_cdk import aws_ec2
from aws_cdk import Fn
from aws_cdk import Tags


class SsmEndpointConstruct(Construct):
    def __init__(self,
                 scope: Construct,
                 id: str,
                 vpc: aws_ec2.Vpc,
                 ) -> None:
        super().__init__(scope, id)

        # ---------------------------------------
        # SSM Private Link
        # ---------------------------------------

        # VPC Endpoint creation for SSM (3 Endpoints needed)
        aws_ec2.InterfaceVpcEndpoint(
            self,
            'SSM Endpoint',
            service=aws_ec2.InterfaceVpcEndpointService(
                Fn.sub('com.amazonaws.${AWS::Region}.ssm')
            ),
            private_dns_enabled=True,
            vpc=vpc,
        )

        aws_ec2.InterfaceVpcEndpoint(
            self,
            'SSM Messages Endpoint',
            service=aws_ec2.InterfaceVpcEndpointService(
                Fn.sub('com.amazonaws.${AWS::Region}.ssmmessages')
            ),
            private_dns_enabled=True,
            vpc=vpc,
        )

        aws_ec2.InterfaceVpcEndpoint(
            self,
            'EC2 Endpoint',
            service=aws_ec2.InterfaceVpcEndpointService(
                Fn.sub('com.amazonaws.${AWS::Region}.ec2')
            ),
            private_dns_enabled=True,
            vpc=vpc,
        )

        aws_ec2.InterfaceVpcEndpoint(
            self,
            'EC2 Messages Endpoint',
            service=aws_ec2.InterfaceVpcEndpointService(
                Fn.sub('com.amazonaws.${AWS::Region}.ec2messages')
            ),
            private_dns_enabled=True,
            vpc=vpc,
        )

        aws_ec2.GatewayVpcEndpoint(
            self,
            'S3 Endpoint',
            vpc=vpc,
            service=aws_ec2.GatewayVpcEndpointAwsService.S3,
            # subnets=[aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PRIVATE_ISOLATED)])
            subnets=[aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_NAT)]
        )
