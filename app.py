#!/usr/bin/env python3
import os
import aws_cdk as cdk
from stacks.vpc_stack import VpcStack
from stacks.ec2_stack import Ec2Stack
from stacks.ssm_document_stack import SsmDocumentStack

env = cdk.Environment(
    account=os.environ.get('CDK_DEPLOY_ACCOUNT', os.environ['CDK_DEFAULT_ACCOUNT']),
    region=os.environ.get('CDK_DEPLOY_REGION', os.environ['CDK_DEFAULT_REGION']),
)

app = cdk.App()

vpc_stack = VpcStack(app, 'VpcStack', env=env)

ec2_stack = Ec2Stack(app, 'Ec2Stack', vpc=vpc_stack.vpc, env=env)
ec2_stack.add_dependency(vpc_stack)

ssm_document_stack = SsmDocumentStack(app, 'SsmAnsibleStack', env=env)
# ssm_document_stack.add_dependency(ec2_stack)  これを削除すべき

app.synth()
