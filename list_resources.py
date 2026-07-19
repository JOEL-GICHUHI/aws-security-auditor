"""
AWS Security Auditor — Stage 1
Connects to your AWS account and lists S3 buckets and EC2 instances.
This is the foundation we'll build security checks on top of.
"""

import boto3
from botocore.exceptions import ClientError


def list_s3_buckets():
    """Return a list of S3 bucket names in the account."""
    s3 = boto3.client("s3")
    try:
        response = s3.list_buckets()
        buckets = [b["Name"] for b in response["Buckets"]]
        return buckets
    except ClientError as e:
        print(f"Error listing S3 buckets: {e}")
        return []


def list_ec2_instances(region="us-east-1"):
    """Return a list of EC2 instance IDs and their state, in a given region."""
    ec2 = boto3.client("ec2", region_name=region)
    instances = []
    try:
        response = ec2.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instances.append({
                    "InstanceId": instance["InstanceId"],
                    "State": instance["State"]["Name"],
                    "InstanceType": instance["InstanceType"],
                })
        return instances
    except ClientError as e:
        print(f"Error listing EC2 instances: {e}")
        return []


def main():
    print("=== S3 Buckets ===")
    buckets = list_s3_buckets()
    if buckets:
        for b in buckets:
            print(f"  - {b}")
    else:
        print("  (none found)")

    print("\n=== EC2 Instances (us-east-1) ===")
    instances = list_ec2_instances()
    if instances:
        for i in instances:
            print(f"  - {i['InstanceId']} | {i['InstanceType']} | {i['State']}")
    else:
        print("  (none found)")


if __name__ == "__main__":
    main()
