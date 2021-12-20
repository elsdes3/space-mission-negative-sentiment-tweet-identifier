#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Manage AWS IAM."""

# pylint: disable=invalid-name,dangerous-default-value

import json
from typing import Dict

import boto3


def create_iam_role(
    iam_role_path: str,
    iam_role_name: str,
    iam_role_description: str,
    iam_role_trust_policy: Dict,
    aws_region: str,
) -> Dict:
    """Create IAM Role."""
    iam_client = boto3.client("iam", region_name=aws_region)
    iam_role_creation_response = iam_client.create_role(
        Path=iam_role_path,
        RoleName=iam_role_name,
        AssumeRolePolicyDocument=json.dumps(iam_role_trust_policy),
        Description=iam_role_description,
        MaxSessionDuration=3600,
    )
    return iam_role_creation_response


def delete_iam_role(iam_role_name: str, aws_region: str) -> Dict:
    """Delete IAM Role."""
    iam_client = boto3.client("iam", region_name=aws_region)
    role_delete_response = iam_client.delete_role(RoleName=iam_role_name)
    return role_delete_response


def check_iam_role_deletion(iam_role_name: str, aws_region: str):
    """Verify Deletion of IAM Role."""
    iam_client = boto3.client("iam", region_name=aws_region)
    iam_roles_list = iam_client.list_roles()["Roles"]
    role_names_list = [role_dict["RoleName"] for role_dict in iam_roles_list]
    assert iam_role_name not in role_names_list
