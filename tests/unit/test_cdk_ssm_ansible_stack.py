import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_ssm_ansible.cdk_ssm_ansible_stack import CdkSsmAnsibleStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_ssm_ansible/cdk_ssm_ansible_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkSsmAnsibleStack(app, "cdk-ssm-ansible")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
