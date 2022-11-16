#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Data combining workflow utilities."""


import os
from typing import Dict, List

import pandas as pd

from file_utils import create_zip_file
from pandas_utils import save_to_parquet
from s3_utils import upload_file_to_s3

# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=dangerous-default-value


def drop_blank_tweets(
    df: pd.DataFrame, subset: List[str] = ["text"]
) -> pd.DataFrame:
    """Drop tweets with no text."""
    df_no_nans = df.dropna(subset=subset)
    num_rows_dropped = len(df) - len(df_no_nans)
    print(f"Dropped {num_rows_dropped:,} tweets from raw data")
    return df_no_nans


def get_hourly_folders_per_day(
    s3_client,
    s3_bucket_name: str,
    path_to_folder: str,
    years_wanted: List[int],
    verbose: bool = False,
) -> List[str]:
    """Get list of S3 hourly data folders, per day of streamed data."""
    list_of_hourly_dirs = []
    for year in years_wanted:
        monthly_prefixes = s3_client.list_objects_v2(
            Bucket=s3_bucket_name,
            Prefix=f"{path_to_folder[1:]}{year}/",
            Delimiter="/",
        )["CommonPrefixes"]
        # print(monthly_prefixes)

        for monthly_prefix in monthly_prefixes:
            daily_prefixes = s3_client.list_objects_v2(
                Bucket=s3_bucket_name,
                Prefix=monthly_prefix["Prefix"],
                Delimiter="/",
            )["CommonPrefixes"]
            # print(monthly_prefix, daily_prefixes)

            for daily_prefix in daily_prefixes:
                hourly_prefixes = s3_client.list_objects_v2(
                    Bucket=s3_bucket_name,
                    Prefix=daily_prefix["Prefix"],
                    Delimiter="/",
                )["CommonPrefixes"]
                # print(
                #     monthly_prefix,
                #     # daily_prefixes,
                #     hourly_prefixes,
                # )
                list_of_hourly_dirs.append(hourly_prefixes)
    list_of_hourly_dirs_flat = [
        sl["Prefix"] for l in list_of_hourly_dirs for sl in l
    ]
    print(f"Found {len(list_of_hourly_dirs_flat):,} hourly folders")
    if verbose:
        for hourly_dirs in list_of_hourly_dirs_flat:
            print(hourly_dirs)
    return list_of_hourly_dirs_flat


def get_hourly_file_name(first_object_key: Dict) -> str:
    """Get name of hourly object on S3."""
    fname = (
        first_object_key["Key"]
        .split("twitter_delivery_stream")[0]
        .split("kinesis-demo")[1]
        .replace("/", "")
    )
    return fname


def get_hourly_files_names(
    s3_client, s3_bucket_name: str, list_of_hourly_dirs_flat: List[str]
):
    """Get year, month, date and hour per hour for hourly S3 objects."""
    keys_yyyymmdd = [
        get_hourly_file_name(
            first_object_key=s3_client.list_objects_v2(
                Bucket=s3_bucket_name, Prefix=list_of_hourly_dirs
            )["Contents"][0]
        )
        for list_of_hourly_dirs in list_of_hourly_dirs_flat
    ]
    file_names = pd.Series(keys_yyyymmdd)
    assert file_names.sort_values().equals(file_names)
    assert len(file_names) == len(list_of_hourly_dirs_flat)
    return file_names


def convert_file_contents_to_df(file_contents_all_flat: List) -> pd.DataFrame:
    """Read contents of streamed file into single-row DataFrame."""
    nested_list_of_records = []
    for file_body in file_contents_all_flat:
        list_of_records = file_body.decode("utf-8").split("\n")[:-1]
        nested_list_of_records.append(list_of_records)
    df = pd.DataFrame(
        [
            record.split("\t")[:-1]
            for sl in nested_list_of_records
            for record in sl
        ]
    )
    return df


def add_column_headers(df: pd.DataFrame, headers: List[str]) -> pd.DataFrame:
    """Add column headers to DataFrame."""
    num_rows, num_cols = df.shape
    print(f"Raw Data contains {num_rows:,} rows and {num_cols:,} columns")
    # df_mismatched = df[~df.iloc[:, -2:].isna().all(axis=1)]
    # mismatched_rows = len(df_mismatched)
    if num_cols == 54:
        df = df.loc[df.iloc[:, -1:].isna().all(axis=1)].drop(columns=[53])
    elif num_cols == 55:
        df = df.loc[df.iloc[:, -2:].isna().all(axis=1)].drop(columns=[53, 54])
    num_new_rows = len(df)
    print(
        f"Dropped {(num_rows - num_new_rows):,} mismatched rows "
        f"out of {num_rows:,}"
    )
    assert df.shape[1] == len(headers)
    df.columns = headers
    return df


def process_single_hour_files(
    s3_client,
    q: int,
    list_of_hourly_dirs: List[str],
    headers: List[str],
    file_name: str,
    len_flat_list_of_hourly_dirs: List[str],
    # tweet_search_terms: List[str],
    # case_sensitive_tweet_search_terms: List[str],
    # joined_tweet_search_terms_no_spaces: List[str],
    # crypto_terms: List[str],
    # religious_terms: List[str],
    # inappropriate_terms: List[str],
    # video_games_terms: List[str],
    # misc_unwanted_terms: List[str],
    # non_english_terms: List[str],
    # min_num_words_tweet: int,
    s3_bucket_name: str,
    processed_data_dir: str,
    # aws_region: str,
    dtypes_dict: Dict,
    verbose: bool = False,
) -> None:
    """Process single hour of file objects on S3."""
    # extract
    objects_hourly_all = s3_client.list_objects_v2(
        Bucket=s3_bucket_name, Prefix=list_of_hourly_dirs
    )
    file_contents_list = []
    for k, file_obj_dict in enumerate(objects_hourly_all["Contents"], 1):
        file_body = s3_client.get_object(
            Bucket=s3_bucket_name, Key=file_obj_dict.get("Key")
        )["Body"].read()
        if verbose:
            print(
                f"Dir {q}/{len_flat_list_of_hourly_dirs} - "
                f"{list_of_hourly_dirs}, reading object "
                f"{k}/{len(objects_hourly_all['Contents'])}"
            )
        file_contents_list.append(file_body)
    print(
        f"Dir {q}/{len_flat_list_of_hourly_dirs} - {list_of_hourly_dirs} "
        f"contains {len(file_contents_list):,} file objects"
    )
    # transform
    df = (
        convert_file_contents_to_df(file_contents_list)
        .pipe(add_column_headers, headers=headers)
        # convert to datetime
        .assign(created_at=lambda df: pd.to_datetime(df["created_at"]))
        .assign(user_joined=lambda df: pd.to_datetime(df["user_joined"]))
        # drop blank tweets
        .pipe(drop_blank_tweets, subset=["text"])
        # # filter based on text in tweet
        # .pipe(
        #     filter_tweets_based_on_content,
        #     tweet_search_terms=tweet_search_terms,
        #     case_sensitive_tweet_search_terms=case_sensitive_tweet_search_terms,
        #     joined_tweet_search_terms_no_spaces=joined_tweet_search_terms_no_spaces,
        #     crypto_terms=crypto_terms,
        #     religious_terms=religious_terms,
        #     inappropriate_terms=inappropriate_terms,
        #     video_games_terms=video_games_terms,
        #     misc_unwanted_terms=misc_unwanted_terms,
        #     non_english_terms=non_english_terms,
        #     # min_num_words_tweet=min_num_words_tweet,
        # )
        # change datatypes
        .astype(dtypes_dict)
    )
    # load
    if "data/" in processed_data_dir:
        # save to .parquet.gzip
        filepath = f"{processed_data_dir}/{file_name}.parquet.gzip"
        storage_options = None
    else:
        filepath = (
            f"s3://{s3_bucket_name}/{processed_data_dir}/{file_name}"
            ".parquet.gzip"
        )
        # storage_options = {
        #     "key": os.getenv("AWS_ACCESS_KEY_ID"),
        #     "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
        # }
    save_to_parquet(df, filepath, storage_options)


def process_files_per_hour(
    s3_client,
    s3_bucket_name: str,
    flat_list_of_hourly_dirs: List[str],
    headers: List[str],
    file_names: List[str],
    # tweet_search_terms: List[str],
    # case_sensitive_tweet_search_terms: List[str],
    # joined_tweet_search_terms_no_spaces: List[str],
    # crypto_terms: List[str],
    # religious_terms: List[str],
    # inappropriate_terms: List[str],
    # video_games_terms: List[str],
    # misc_unwanted_terms: List[str],
    # non_english_terms: List[str],
    # min_num_words_tweet: int,
    processed_data_dir: str,
    proc_zip_fname: str,
    path_to_folder: str,
    aws_region: str,
    dtypes_dict: Dict,
    cleanup_local_files: bool = False,
    upload_to_s3: bool = False,
    verbose: bool = False,
) -> None:
    """Run ETL workflow to process hourly streamed tweets."""
    for q, (file_name, list_of_hourly_dirs) in enumerate(
        zip(file_names, flat_list_of_hourly_dirs), 1
    ):
        process_single_hour_files(
            s3_client,
            q,
            list_of_hourly_dirs,
            headers,
            file_name,
            len(flat_list_of_hourly_dirs),
            # tweet_search_terms,
            # case_sensitive_tweet_search_terms,
            # joined_tweet_search_terms_no_spaces,
            # crypto_terms,
            # religious_terms,
            # inappropriate_terms,
            # video_games_terms,
            # misc_unwanted_terms,
            # non_english_terms,
            # min_num_words_tweet,
            s3_bucket_name,
            processed_data_dir,
            # aws_region,
            dtypes_dict,
            verbose,
        )
        if q < len(flat_list_of_hourly_dirs):
            print()

    # (if saved locally) zip all processed data files, upload to S3, delete
    # local files
    if "data/" in processed_data_dir:
        if upload_to_s3:
            # create zip of all .parquet.gzip processed data files
            curr_dir = os.getcwd()
            create_zip_file(
                "*.parquet.gzip", processed_data_dir, proc_zip_fname
            )
            # upload zip file to S3 bucket
            try:
                assert os.getcwd() == curr_dir
                upload_file_to_s3(
                    aws_region,
                    processed_data_dir,
                    proc_zip_fname,
                    s3_bucket_name,
                    f"{path_to_folder[1:-1]}/processed/{proc_zip_fname}",
                )
                print("\nUploaded zipped file to S3 bucket")
            except AssertionError as e:
                print(
                    f"\n{str(e)}: Incorrect working directory. "
                    "Did not upload zipped file to S3 bucket."
                )

        if cleanup_local_files:
            # delete locally exported parquet files
            list(
                map(
                    os.remove,
                    [
                        os.path.join(processed_data_dir, f"{f}.parquet.gzip")
                        for f in file_names
                    ],
                )
            )
    if cleanup_local_files:
        print("Deleted local .parquet.gzip files with filtered data.")
        # delete local zip file
        os.remove(os.path.join(processed_data_dir, proc_zip_fname))
        print("Deleted local .zip file created from all filtered data files.")
