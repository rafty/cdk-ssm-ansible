import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.ssm_document_stack import CdkSsmAnsibleStack

# example tests. To run these tests, uncomment this file along with the example
# resource in stacks/ssm_document_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkSsmAnsibleStack(app, "cdk-ssm-ansible")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
