from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_dynamodb as dynamodb,
    aws_ssm as ssm
)


class SharedStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create dynamo table
        my_table = dynamodb.Table(
            self, "DynamoTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # print("my_table",my_table.table_arn)
    
        ssm.StringParameter(
            self, 'DynamoTableSSM',
            parameter_name="/dev/dbserver/dynamodb/db-arn",
            string_value=my_table.table_arn
        )

        # create vpc
        vpc = ec2.Vpc(
            self, "Vpc",
            max_azs=2
        )

        ssm.StringParameter(
            self, 'VpcSSM',
            parameter_name="/dev/network/vpc/vpc-id",
            string_value=vpc.vpc_id
        )

        # create ecs cluster
        cluster = ecs.Cluster(
            self, 'Cluster',
            vpc=vpc
        )

        ssm.StringParameter(self, 'EcsClusterSSM',
            parameter_name="/dev/compute/container/ecs-cluster-arn",
            string_value=cluster.cluster_arn
        )