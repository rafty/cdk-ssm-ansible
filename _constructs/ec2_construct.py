from constructs import Construct
from aws_cdk import aws_ec2
from aws_cdk import aws_iam
from aws_cdk import Tags


class Ec2InstanceConstruct(Construct):
    def __init__(self,
                 scope: Construct,
                 id: str,
                 vpc: aws_ec2.Vpc
                 ) -> None:
        super().__init__(scope, id)

        # Security Group
        my_security_group = aws_ec2.SecurityGroup(
            self,
            'SecurityGroup',
            security_group_name='test-sg',
            vpc=vpc,
            description='Allow ssh access to ec2 instances from anywhere',
            allow_all_outbound=True
        )
        my_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.any_ipv4(),
            connection=aws_ec2.Port.tcp(22),
            description='allow public ssh access'
        )
        my_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.any_ipv4(),
            connection=aws_ec2.Port.tcp(80),
            description='allow HTTP traffic from anywhere'
        )
        my_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.any_ipv4(),
            connection=aws_ec2.Port.tcp(443),
            description='allow HTTPS traffic from anywhere'
        )
        # Security Group

        aws_ami = aws_ec2.AmazonLinuxImage(
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            cpu_type=aws_ec2.AmazonLinuxCpuType.X86_64
        )

        # instance_type = aws_ec2.InstanceType.of(
        #     instance_class=aws_ec2.InstanceClass.T2,
        #     # instance_size=aws_ec2.InstanceSize.NANO
        #     instance_size=aws_ec2.InstanceSize.MICRO
        # )
        instance_type = aws_ec2.InstanceType('t3.micro')

        role = aws_iam.Role(
            self,
            'SsmStateManagerAnsible',
            assumed_by=aws_iam.ServicePrincipal('ec2.amazonaws.com'),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3ReadOnlyAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchAgentServerPolicy'),
            ]
        )

        # vpc_subnets_private = aws_ec2.SubnetSelection(
        #     subnets=[
        #         aws_ec2.Subnet.from_subnet_attributes(
        #             self,
        #             'SubnetList',
        #             availability_zones='ap-northeast-1a',
        #             subnet_id='subnet-xxxxxx'
        #         )
        #     ]
        # )

        ec2_instance = aws_ec2.Instance(
            self,
            'EC2Instance',
            instance_name='SsmTest',
            vpc=vpc,
            # vpc_subnets=aws_ec2.SubnetSelection(subnets=),  # Default: - Private subnets. TODO
            instance_type=instance_type,
            machine_image=aws_ami,
            security_group=my_security_group,
            role=role
        )
        Tags.of(ec2_instance).add('ansible', 'play')
