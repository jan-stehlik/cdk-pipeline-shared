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

        # requied vpc id to retrieve vpc info using vpc from attributres method on dependent stack
        ssm.StringParameter(
            self, 'VpcIdSSM',
            parameter_name="/dev/network/vpc/vpc-id",
            string_value=vpc.vpc_id
        )

        # requied vpc az's to retrieve vpc info using vpc from attributres method on dependent stack
        ssm.StringListParameter(
            self, 'VpcAvailabilityZonesSSM',
            parameter_name="/dev/network/vpc/vpc-az",
            string_list_value=vpc.availability_zones
        )

        # requied vpc az's to retrieve vpc info using vpc from attributres method on dependent stack
        ssm.StringListParameter(
            self, 'VpcPublicSubnetsSSM',
            parameter_name="/dev/network/vpc/vpc-public-subnets",
            string_list_value=[vpc.public_subnets[0].subnet_id,vpc.public_subnets[1].subnet_id]
        )

        # requied security group name to retrieve ecs cluster info
        vpc_sgp = vpc.node.default_child.__getattribute__(
            "attr_default_security_group")

        ssm.StringParameter(
            self, 'SgIdSSM',
            parameter_name="/dev/network/vpc/security-group-id",
            string_value=vpc_sgp
        )

        # create ecs cluster
        cluster = ecs.Cluster(
            self, 'Cluster',
            vpc=vpc
        )

        # requied security group name to retrieve ecs cluster info
        ssm.StringParameter(self, 'EcsClusterNameSSM',
            parameter_name="/dev/compute/container/ecs-cluster-name",
            string_value=cluster.cluster_name
        )