#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Transformer model inference utilities."""


import os
from glob import glob

import dask.dataframe as dd
import pandas as pd

from model_utils import calculate_metrics
from s3_utils import download_file_from_s3, extract_zip_file

# pylint: disable=invalid-name,dangerous-default-value
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments


def get_metadata(
    s3_client,
    data,
    processed_data_dir,
    proc_text_zip_fname,
    s3_bucket_name,
    path_to_folder,
    aws_region,
    dtypes_dict_proc_data,
    cols_to_use,
    needs_support_labels,
):
    """."""
    # Get metadata files
    if not os.path.exists(
        os.path.join(processed_data_dir, proc_text_zip_fname)
    ):
        fname_no_ext = os.path.splitext(proc_text_zip_fname)[0]
        fpath = f"{path_to_folder[1:]}processed/{fname_no_ext}"
        download_file_from_s3(
            s3_client,
            s3_bucket_name,
            path_to_folder,
            processed_data_dir,
            proc_text_zip_fname,
            aws_region,
            fpath,
        )
        output_fname_no_ext = os.path.splitext(proc_text_zip_fname)[0]
        output_fpath = (
            f"{processed_data_dir}/{output_fname_no_ext}.parquet.gzip"
        )
        extract_zip_file(
            os.path.join(processed_data_dir, proc_text_zip_fname),
            output_fpath,
        )
    proc_files_meta = glob(f"{processed_data_dir}/*.parquet.gzip")
    proc_files_meta_all = glob(
        f"{processed_data_dir}/*.parquet.gzip/*.gz.parquet"
    )

    # Get metadata
    df_metadata = (
        dd.read_parquet(proc_files_meta)
        .reset_index(drop=True)
        .astype(dtypes_dict_proc_data)
        .set_index("created_at")  # sorts DataFrame based on this column
        .reset_index()
        .repartition(npartitions=len(proc_files_meta_all))[cols_to_use]
        .compute()
    )

    df_metadata = (
        data.merge(
            df_metadata.drop_duplicates(subset=["id", "created_at", "text"]),
            on=["id", "created_at", "text"],
            how="left",
        )
        .rename(columns={"sentiment": "labels"})
        .assign(
            labels=lambda df: df["labels"]
            .isin(needs_support_labels)
            .astype("int32")
        )
    )
    assert len(data) == len(df_metadata)
    df_metadata["text"] = (
        df_metadata["text"]
        .str.lstrip()
        .str.rstrip()
        .str.replace("&gt;", ">")
        .str.replace("&lt;", "<")
        .str.replace("&amp;", "&")
    )
    return df_metadata


def extract_metadata_features(
    df_metadata, dt_bins, dt_labels, country_mapper_dict
):
    """."""
    # Feature engineering for metadata
    df_metadata = (
        df_metadata.assign(
            created_at_hour=lambda df: df["created_at"].dt.hour.astype(
                pd.Int32Dtype()
            )
        )
        .assign(
            created_at_day=lambda df: df["created_at"]
            .dt.day_name()
            .astype(pd.StringDtype())
        )
        .assign(
            user_joined_hour=lambda df: df["user_joined"].dt.hour.astype(
                pd.Int32Dtype()
            )
        )
        .assign(
            user_joined_day=lambda df: df["user_joined"]
            .dt.day_name()
            .astype(pd.StringDtype())
        )
        .assign(
            created_at_time_of_day=lambda df: pd.cut(
                df["created_at_hour"],
                bins=dt_bins,
                labels=dt_labels,
                include_lowest=True,
            )
        )
    )
    df_metadata["country"] = "Other"
    for k, v in country_mapper_dict.items():
        mask = df_metadata["user_location"].str.contains("|".join(v))
        df_metadata.loc[mask, "country"] = k
    df_metadata["country"] = df_metadata["country"].astype(pd.StringDtype())
    # Verify that a country is present for every row of metadata
    assert df_metadata["country"].value_counts().sum() == len(df_metadata)
    return df_metadata


def evaluate_inference(df_infer, label_mapper, batch_num, df_meta, id2label):
    """."""
    df_fn_error = df_infer.query("(labels == 1) & (pred != 1)")
    num_fn = len(df_fn_error)
    frac_fn = 100 * len(df_fn_error) / len(df_infer.query("labels == 1"))
    num_minority_samples = len(df_infer.query("labels == 1"))

    df_fp_error = df_infer.query("(labels != 1) & (pred == 1)")
    num_fp = len(df_fp_error)
    frac_fp = 100 * len(df_fp_error) / len(df_infer.query("labels != 1"))
    num_pred_minority_samples = len(df_infer.query("labels != 1"))

    metrics_dict, df_cm, df_cr = calculate_metrics(
        df_infer["labels"].to_numpy(),
        df_infer["pred"].to_numpy(),
        list(label_mapper.values()),
        list(label_mapper.keys()),
        "weighted",
        0,
        use_sample_weights=False,
    )
    df_cm = df_cm.assign(batch_num=batch_num)
    df_metrics = pd.DataFrame.from_dict(metrics_dict, orient="index").T.assign(
        batch_num=batch_num
    )
    df_cr = df_cr.merge(
        df_meta["labels"]
        .value_counts(normalize=True)
        .rename("freq")
        .reset_index()
        .assign(index=lambda df: df["index"].map(id2label))
        .set_index("index"),
        left_index=True,
        right_index=True,
        how="left",
    ).assign(batch_num=batch_num)
    return [
        num_fn,
        frac_fn,
        num_minority_samples,
        num_fp,
        frac_fp,
        num_pred_minority_samples,
        df_metrics,
        df_cm,
        df_cr,
    ]
