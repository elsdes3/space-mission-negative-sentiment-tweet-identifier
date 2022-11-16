#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""AWS Python SDK storage utilities."""


import os
import zipfile
from datetime import datetime
from typing import List, Union

import boto3

# pylint: disable=invalid-name
# pylint: disable=too-many-arguments


def download_file_from_s3(
    s3_client,
    s3_bucket_name: str,
    # path_to_folder: str,
    data_dir: str,
    fname: str,
    aws_region: str,
    prefix: str,
) -> None:
    """Download file from S3."""
    dest_filepath = os.path.join(data_dir, fname)
    s3_filepath_key = s3_client.list_objects_v2(
        Bucket=s3_bucket_name,
        Delimiter="/",
        Prefix=prefix,
    )["Contents"][0]["Key"]
    start = datetime.now()
    print(
        f"Started downloading processed data zip file from {s3_filepath_key} "
        f"to {dest_filepath} at {start.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
        "..."
    )
    s3 = boto3.resource("s3", region_name=aws_region)
    s3.meta.client.download_file(
        s3_bucket_name,
        s3_filepath_key,
        dest_filepath,
    )
    duration = (datetime.now() - start).total_seconds()
    print(f"Done downloading in {duration:.3f} seconds.")


def extract_zip_file(dest_filepath: str, data_dir: str) -> None:
    """."""
    start = datetime.now()
    print(
        "Started extracting filtered data parquet files from "
        f"processed data zip file to {data_dir} at "
        f"{start.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}..."
    )
    zip_ref = zipfile.ZipFile(dest_filepath)
    zip_ref.extractall(data_dir)
    zip_ref.close()
    duration = (datetime.now() - start).total_seconds()
    print(f"Done extracting in {duration:.3f} seconds.")


def download_files_from_s3(
    s3_client,
    s3_bucket_name: str,
    data_dir: str,
    aws_region: str,
    prefix: str,
    fext_wanted: Union[str, None] = None,
) -> None:
    """Download files from S3."""
    s3_fpath_contents = s3_client.list_objects_v2(
        Bucket=s3_bucket_name,
        Delimiter="/",
        Prefix=prefix,
    )["Contents"]

    if fext_wanted:
        s3_filepath_keys = [
            fc["Key"] for fc in s3_fpath_contents if fext_wanted in fc["Key"]
        ]
    else:
        s3_filepath_keys = [fc["Key"] for fc in s3_fpath_contents]

    for s3_filepath_key in s3_filepath_keys:
        dest_filepath = os.path.join(
            data_dir, os.path.basename(s3_filepath_key)
        )
        if not os.path.exists(dest_filepath):
            start = datetime.now()
            start_time_str = start.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print(
                f"Started downloading file from {s3_filepath_key} to "
                f"{dest_filepath} at {start_time_str}..."
            )
            s3 = boto3.resource("s3", region_name=aws_region)
            s3.meta.client.download_file(
                s3_bucket_name,
                s3_filepath_key,
                dest_filepath,
            )
            duration = (datetime.now() - start).total_seconds()
            print(f"Done downloading in {duration:.3f} seconds.")
        else:
            print(f"File found at {dest_filepath}. Did nothing.")


def upload_file_to_s3(
    aws_region: str,
    processed_data_dir: str,
    fname: str,
    s3_bucket_name: str,
    s3_key: str,
) -> None:
    """Upload file to key in S3 bucket."""
    s3_resource = boto3.resource("s3", region_name=aws_region)
    s3_resource.meta.client.upload_file(
        f"{processed_data_dir}/{fname}",
        s3_bucket_name,
        s3_key,
    )


def get_s3_bucket_file_list(
    s3_client, s3_bucket_name: str, processed_data_dir: str
) -> List[str]:
    """Get list of all filepaths in folder in S3 bucket."""
    print(f"Getting list of files in {processed_data_dir} in S3 bucket...")
    s3_processed_data_filepaths = [
        f"s3://{s3_bucket_name}/{c['Key']}"
        for c in s3_client.list_objects_v2(
            Bucket=s3_bucket_name,
            Delimiter="/",
            Prefix=f"{processed_data_dir}/",
        )["Contents"]
    ]
    print("Done.")
    return s3_processed_data_filepaths
