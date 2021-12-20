#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Programmatic execution of notebooks."""

# pylint: disable=invalid-name

import argparse
import os
from datetime import datetime
from typing import Dict, List

import papermill as pm

PROJ_ROOT_DIR = os.getcwd()
data_dir = os.path.join(PROJ_ROOT_DIR, "data")
output_notebook_dir = os.path.join(PROJ_ROOT_DIR, "executed_notebooks")

raw_data_path = os.path.join(data_dir, "raw")

one_dict_nb_name = "1_create_aws_resources.ipynb"
two_dict_nb_name = "2_delete_aws_resources.ipynb"

firehose_stream_name = "twitter_delivery_stream"

one_dict = dict(
    s3_bucket_name="testwillz3s",
    iam_role_path="/",
    iam_role_name="ec2-dummy-role",
    iam_role_description="BOTO3 ec2 dummy role",
    iam_role_trust_policy={
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {"Service": "firehose.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    },
    stream_s3_destination_prefix="datasets/twitter/kinesis-demo/YYYY/MM/dd/HH",
    firehose_stream_name="twitter_delivery_stream",
    cw_logs_group_name=f"kinesisfirehose_{firehose_stream_name}",
    sg_group_tags=[{"Key": "Name", "Value": "allow-inbound-ssh"}],
    key_fname="aws_ec2_key",
    keypair_name="ec2-key-pair",
    ec2_instance_image_id="ami-0cc00ed857256d2b4",
    ec2_instance_type="t2.micro",
    ec2_instance_tags_list=[{"Key": "Name", "Value": "my-ec2-instance"}],
)
two_dict = dict(
    s3_bucket_name="testwillz3s",
    iam_role_name="ec2-dummy-role",
    firehose_stream_name=firehose_stream_name,
    cw_logs_group_name=f"kinesisfirehose_{firehose_stream_name}",
    sg_group_tags=[{"Key": "Name", "Value": "allow-inbound-ssh"}],
    key_fname="aws_ec2_key",
    keypair_name="ec2-key-pair",
    ec2_instance_tags_list=[{"Key": "Name", "Value": "my-ec2-instance"}],
)


def papermill_run_notebook(
    nb_dict: Dict, output_notebook_directory: str = "executed_notebooks"
) -> None:
    """Execute notebook with papermill"""
    for notebook, nb_params in nb_dict.items():
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_nb = os.path.basename(notebook).replace(
            ".ipynb", f"-{now}.ipynb"
        )
        print(
            f"\nInput notebook path: {notebook}",
            f"Output notebook path: {output_notebook_directory}/{output_nb} ",
            sep="\n",
        )
        for key, val in nb_params.items():
            print(key, val, sep=": ")
        pm.execute_notebook(
            input_path=notebook,
            output_path=f"{output_notebook_directory}/{output_nb}",
            parameters=nb_params,
        )


def run_notebooks(
    notebooks_list: List, output_notebook_directory: str = "executed_notebooks"
) -> None:
    """Execute notebooks from CLI.
    Parameters
    ----------
    nb_dict : List
        list of notebooks to be executed
    Usage
    -----
    > import os
    > PROJ_ROOT_DIR = os.path.abspath(os.getcwd())
    > one_dict_nb_name = "a.ipynb
    > one_dict = {"a": 1}
    > run_notebook(
          notebook_list=[
              {os.path.join(PROJ_ROOT_DIR, one_dict_nb_name): one_dict}
          ]
      )
    """
    for nb in notebooks_list:
        papermill_run_notebook(
            nb_dict=nb, output_notebook_directory=output_notebook_directory
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--action",
        type=str,
        dest="action",
        default="create",
        help="whether to create or destroy AWS resources",
    )
    args = parser.parse_args()

    nb_dict_list = [one_dict] if args.action == "create" else [two_dict]
    nb_name_list = (
        [one_dict_nb_name] if args.action == "create" else [two_dict_nb_name]
    )
    notebook_list = [
        {os.path.join(PROJ_ROOT_DIR, nb_name): nb_dict}
        for nb_dict, nb_name in zip(nb_dict_list, nb_name_list)
    ]
    run_notebooks(
        notebooks_list=notebook_list,
        output_notebook_directory=output_notebook_dir,
    )
