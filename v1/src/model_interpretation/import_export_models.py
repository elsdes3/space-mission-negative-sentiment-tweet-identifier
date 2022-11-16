#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Utilities to import and export a trained ML model."""


from datetime import datetime
from typing import List

import boto3


def get_all_saved_vectorizer_models_from_s3(
    s3_bucket_name: str,
    region: str,
    prefix: str,
    vectorizer_folder_partial_name: str,
) -> List[str]:
    """Get paths to sub-folder containing vectorizer, in S3 bucket."""
    s3_client = boto3.client("s3", region_name=region)
    models_subfolder_contents_response = s3_client.list_objects_v2(
        Bucket=s3_bucket_name,
        Prefix=prefix,
        Delimiter="/",
    )
    # Get paths to all save vectorizer model folders
    vectorizer_fpaths = [
        sub_folder["Prefix"]
        for sub_folder in models_subfolder_contents_response.get(
            "CommonPrefixes", []
        )
        if vectorizer_folder_partial_name in sub_folder["Prefix"]
    ]
    # Sort paths by timestamp in suffix of folder name
    vectorizer_fpaths = sorted(
        vectorizer_fpaths,
        key=lambda s: datetime.strptime(s[:-1][-15:], "%Y%m%d_%H%M%S"),
    )
    return vectorizer_fpaths
