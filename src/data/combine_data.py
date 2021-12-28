#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Combine raw tweets data, per hour, into single CSV file."""

# pylint: disable=invalid-name,too-many-locals,too-many-arguments

import os
from datetime import datetime
from io import StringIO
from typing import Dict, List, Union

import boto3
import pandas as pd


def get_objects_in_one_s3_level(
    s3b_name: str, content: Union[Dict, str], region: str
) -> Dict:
    """Get list of all storage objects in single S3 level."""
    s3_client = boto3.client("s3", region_name=region)
    prefix = content if isinstance(content, str) else content.get("Prefix")
    response_new = s3_client.list_objects_v2(
        Bucket=s3b_name, Prefix=prefix, Delimiter="/"
    )
    return response_new


def get_data_metadata(file: str, s3_bucket_name: str, region: str) -> Dict:
    """Extract data and file metadata from raw tweets data."""
    s3_client = boto3.client("s3", region_name=region)
    file_body = s3_client.get_object(
        Bucket=s3_bucket_name, Key=file.get("Key")
    )["Body"].read()
    file_name = os.path.basename(file["Key"])
    return {"file_body": file_body, "file_name": file_name}


def get_datetime_string() -> str:
    """Generate current timestamp as string."""
    return datetime.now().strftime("%Y%m%d%H%M%S")


def get_hourly_data_metadata(
    data_list: List, headers: List, fpath: str, get_metadata_agg: bool = False
) -> List[pd.DataFrame]:
    """Load raw tweets data and file metadata into DataFrames."""
    year, month, day, hour = fpath.split("/", 3)[-1].split("/", 3)
    dfs = []
    dfs_metadata = []
    for k, raw_data_contents in enumerate(data_list):
        single_buffer_data_strings = (
            raw_data_contents["file_body"].decode("utf-8").split("\n")
        )
        all_buffer_contents = []
        for q, data_string in enumerate(single_buffer_data_strings):
            if data_string:
                values = data_string.strip().split("\t")
                # print(
                #     k+1,
                #     q+1,
                #     len(raw_data_contents["file_body"]),
                #     len(values),
                #     len(values) != len(headers),
                #     data_string,
                # )
                dfs_metadata.append(
                    {
                        "file": k + 1,
                        "file_name": raw_data_contents["file_name"],
                        "encoded_length": len(raw_data_contents["file_body"]),
                        "values_index": q + 1,
                        "len_values": len(values),
                        "malformed_values": len(values) != len(headers),
                        "file_year": year,
                        "file_month": month,
                        "file_day": day,
                        "file_hour": hour[:-1],
                    }
                )
                if len(values) == len(headers):
                    all_buffer_contents.append(values)
        df_row = pd.DataFrame(all_buffer_contents, columns=headers)
        dfs.append(df_row)
    df = pd.concat(dfs, ignore_index=True).dropna()
    df_metadata = pd.DataFrame.from_records(dfs_metadata)
    if get_metadata_agg:
        df_metadata_agg = (
            df_metadata.groupby(["file_name"], as_index=False)
            .agg(
                {
                    "encoded_length": "min",
                    "values_index": "max",
                    "len_values": "min",
                    "malformed_values": "sum",
                }
            )
            .assign(num_valid_records=len(df))
        )
    else:
        df_metadata_agg = pd.DataFrame()
    return [df, df_metadata, df_metadata_agg]


def create_folder_in_s3_bucket(
    region: str, s3_bucket_name: str, folder_name: str = "csvs"
) -> None:
    """Create folder in S3 bucket, if it does not exist."""
    s3_client = boto3.client("s3", region_name=region)
    folders_response_result = s3_client.list_objects_v2(
        Bucket=s3_bucket_name,
        Prefix="datasets/twitter/kinesis-demo/csvs",
        Delimiter="/",
    )
    if "CommonPrefixes" in folders_response_result:
        print(
            f"Found existing folder {folder_name} in {s3_bucket_name}. "
            "Did nothing."
        )
    else:
        proc_data_folder_creation_response = s3_client.put_object(
            Bucket=s3_bucket_name,
            Body="",
            Key="datasets/twitter/kinesis-demo/csvs/",
        )
        print(f"Created folder csvs in {s3_bucket_name}.")


def get_existing_csv_files_list(
    s3_bucket_name: str, region: str, prefix: str
) -> List[str]:
    """Get list of files in subfolder in S3 bucket."""
    s3_resource = boto3.resource("s3", region_name=region)
    bucket = s3_resource.Bucket(s3_bucket_name)
    files_found_objects_list = list(bucket.objects.filter(Prefix=prefix))
    files_found_names_list = [w.key for w in files_found_objects_list]
    return files_found_names_list


def save_df_to_csv_on_s3(
    df: pd.DataFrame,
    bucket_name: str,
    filepath: str,
    region: str,
    df_type: str = "metadata",
) -> None:
    """Export DataFrame as CSV to folder in S3 bucket."""
    s3_client = boto3.client("s3", region_name=region)
    csv_buf = StringIO()
    df.to_csv(csv_buf, header=True, index=False)
    csv_buf.seek(0)
    s3_client.put_object(
        Bucket=bucket_name, Body=csv_buf.getvalue(), Key=filepath
    )
    print(
        f"- Copied {len(df):,} rows of {df_type} to bucket {bucket_name} "
        f"at {filepath}."
    )


def save_data_and_metadata_to_s3_csv(
    subfolder_path: str,
    existing_csv_files: List[str],
    s3_bucket_name: str,
    headers: List[str],
    content: Dict,
    path_to_csvs_folder: str,
    region: str,
) -> None:
    """Extract tweets data and file metadata to csvs/ in S3 bucket."""
    ctime_str = "hc" + subfolder_path.split("/", 3)[-1].rstrip("/").replace(
        "/", ""
    )
    ftime_str = "s" + get_datetime_string()
    existing_matching_csv_files = [
        f for f in existing_csv_files if ctime_str in f
    ]
    if not existing_matching_csv_files:
        # Get nested list of data
        data_list = [
            get_data_metadata(file_name, s3_bucket_name, region)
            for file_name in get_objects_in_one_s3_level(
                s3_bucket_name,
                content,
                region,
            )["Contents"]
        ]
        # Get tweets data and metadata
        df, df_metadata, _ = get_hourly_data_metadata(
            data_list, headers, content.get("Prefix")
        )
        # Change datetime format
        for c in ["created_at", "user_joined"]:
            df[c] = pd.to_datetime(df[c])
        # Save data and metadata
        for df_obj, suffix, file_type in zip(
            [df, df_metadata],
            ["tweets_", "tweets_metadata_"],
            ["data", "metadata"],
        ):
            fpath = (
                f"{path_to_csvs_folder}csvs/{suffix}"
                f"{len(data_list)}_{ctime_str}_{ftime_str}.csv"
            )
            print(f"Did not find {file_type} CSV file in {fpath}. ")
            save_df_to_csv_on_s3(
                df_obj, s3_bucket_name, fpath, region, file_type
            )
    else:
        fpath = existing_matching_csv_files[0]
        print(f"Found CSV file in {fpath}. Did nothing.")
