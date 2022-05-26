from ..util.Util import generate_word, generate_password

import os
import boto3
from faker import Faker


class Moonraker:
    """
    A class used to represent a Configuration object

    Attributes
    ----------
    workmail

    Methods
    -------
    """

    def __init__(self):
        """
        Class init

        Parameters
        ----------
        """
        self.ec2 = boto3.client("ec2", region_name="us-west-2")

    def create_key_pair(self):
        """ """
        key_pair = self.ec2.create_key_pair(KeyName="ec2-key-pair")
        private_key = key_pair["KeyMaterial"]
        # write private key to file with 400 permissions
        with os.fdopen(
            os.open("aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+"
        ) as handle:
            handle.write(private_key)

    def create_instance(self):
        """ """
        instances = self.ec2.run_instances(
            ImageId="ami-0b0154d3d8011b0cd",
            MinCount=1,
            MaxCount=1,
            InstanceType="t4g.nano",
            KeyName="ec2-key-pair",
        )
        print(instances["Instances"][0]["InstanceId"])

    def get_public_ip(self, instance_id):
        """ """
        reservations = self.ec2.describe_instances(InstanceIds=[instance_id]).get(
            "Reservations"
        )
        for reservation in reservations:
            for instance in reservation["Instances"]:
                print(instance.get("PublicIpAddress"))

    def get_running_instances(self):
        """ """
        reservations = self.ec2.describe_instances(
            Filters=[
                {
                    "Name": "instance-state-name",
                    "Values": ["running"],
                }
            ]
        ).get("Reservations")
        #
        for reservation in reservations:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                public_ip = instance["PublicIpAddress"]
                private_ip = instance["PrivateIpAddress"]
                print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")

    def stop_instance(self, instance_id):
        """ """
        response = self.ec2.stop_instances(InstanceIds=[instance_id])
        print(response)

    def terminate_instance(self, instance_id):
        """ """
        response = self.ec2.terminate_instances(InstanceIds=[instance_id])
        print(response)


class LoveAtLast:
    """A class used to represent a Configuration object

    Attributes
    ----------
    workmail

    Methods
    -------
    """

    def __init__(self):
        """Class init

        Parameters
        ----------
        """
        self.workmail = boto3.client("workmail")

    def create_user(self, organization_id):
        """ """
        faker = Faker()
        display_name = faker.name()
        user_name = ".".join(display_name.split(" "))
        response = self.workmail.create_user(
            OrganizationId=organization_id,
            Name=user_name,
            DisplayName=display_name,
            Password=generate_password(),
        )

    def delete_user(self, organization_id, user_id):
        """ """
        response = self.workmail.delete_user(
            OrganizationId=organization_id, UserId=user_id
        )

    def describe_user(self, organization_id, user_id):
        """ """
        response = self.workmail.delete_user(
            OrganizationId=organization_id, UserId=user_id
        )

    def create_organization(self):
        """ """
        organization_alias = generate_word()
        response = self.workmail.create_organization(Alias=organization_alias)

    def delete_organization(self, organization_id):
        """ """
        response = self.workmail.delete_organization(
            # ClientToken='string',
            OrganizationId=organization_id,
            DeleteDirectory=True,
        )
