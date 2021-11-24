import os
import random
import string
import boto3

def generate_password(length):
    """
    """
    all = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.sample(all,length))


class  Moonraker:
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
        """
        """
        key_pair = self.ec2.create_key_pair(KeyName="ec2-key-pair")
        private_key = key_pair["KeyMaterial"]
        # write private key to file with 400 permissions
        with os.fdopen(os.open("/tmp/aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
            handle.write(private_key)

    def create_instance(self):
        """
        """
        instances = self.ec2.run_instances(
            ImageId="ami-0b0154d3d8011b0cd",
            MinCount=1,
            MaxCount=1,
            InstanceType="t4g.nano",
            KeyName="ec2-key-pair"
        )
        print(instances["Instances"][0]["InstanceId"])

    def get_public_ip(self, instance_id):
        """
        """
        reservations = self.ec2.describe_instances(InstanceIds=[instance_id]).get("Reservations")
        for reservation in reservations:
            for instance in reservation['Instances']:
                print(instance.get("PublicIpAddress"))

    def get_running_instances(self):
        """
        """
        reservations = self.ec2.describe_instances(Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"],
            }
        ]).get("Reservations")
        #
        for reservation in reservations:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                public_ip = instance["PublicIpAddress"]
                private_ip = instance["PrivateIpAddress"]
                print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")

    def stop_instance(self, instance_id):
        """
        """
        response = self.ec2.stop_instances(InstanceIds=[instance_id])
        print(response)

    def terminate_instance(self, instance_id):
        """
        """
        response = self.ec2.terminate_instances(InstanceIds=[instance_id])
        print(response)


class LoveAtLast:
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
        self.workmail = boto3.client('workmail')

    def create_user(self):
        """
        """
        response = self.workmail.create_user(
            OrganizationId='string',
            Name='string',
            DisplayName='string',
            Password='string'
        )

    def delete_user(self):
        """
        """
        response = self.workmail.delete_user(
            OrganizationId='string',
            UserId='string'
        )

    def describe_user(self):
        """
        """
        response = self.workmail.delete_user(
            OrganizationId='string',
            UserId='string'
        )

    def create_organization(self):
        """
        """
        response = self.workmail.create_organization(
            DirectoryId='string',
            Alias='string',
            ClientToken='string',
            Domains=[
                {
                    'DomainName': 'string',
                    'HostedZoneId': 'string'
                },
            ],
            KmsKeyArn='string',
            EnableInteroperability=True|False
        )

    def delete_organization(self):
        """
        """
        response = self.workmail.delete_organization(
            ClientToken='string',
            OrganizationId='string',
            DeleteDirectory=True|False
        )
