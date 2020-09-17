from aws_cdk.core import Construct, Stack, Stage, Environment
from cdk_pipeline_shared.SharedStack import SharedStack

class SharedStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        shared_stack = SharedStack(self, "SharedStack")