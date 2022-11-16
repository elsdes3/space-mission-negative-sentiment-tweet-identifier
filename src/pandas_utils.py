#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Pandas DataFrame utilities."""


import os
from typing import Dict, List, Union

import pandas as pd

# pylint: disable=invalid-name


def save_to_parquet(
    df: pd.DataFrame,
    filepath: str,
    storage_options: Union[None, Dict[str, str]] = None,
) -> None:
    """Save DataFrame to .parquet.gzip file."""
    print(f"Saving to parquet file {os.path.basename(filepath)}...")
    df.to_parquet(filepath, index=False, storage_options=storage_options)
    print("Done.")


def read_parquet(
    filepath: str,
    columns: Union[None, List[str]] = None,
    storage_options: Union[None, Dict[str, str]] = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """Read DataFrame from .parquet.gzip file."""
    df = pd.read_parquet(
        filepath, columns=columns, storage_options=storage_options
    )
    if verbose:
        print(
            f"Read {len(df):,} rows of data from parquet "
            f"file {os.path.basename(filepath)}"
        )
    return df


def calc_pct_change_for_time_cols(df, time_cols, pred_type_col):
    """Calculate percent change between models for time-related columns."""
    df_pct_reduced = (
        df.set_index(pred_type_col)[time_cols]
        .T.assign(
            pct_reduced=lambda df: 100 * (df["naive"] - df["ML"]) / df["naive"]
        )
        .T.reset_index()
        .assign(batch_num=df["batch_num"].iloc[0])
        .assign(total_number_tweets=df["total_number_tweets"].iloc[0])
    )
    return df_pct_reduced
