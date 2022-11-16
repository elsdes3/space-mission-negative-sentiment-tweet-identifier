#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Text processing workflow utilities."""


import os
from datetime import datetime
from typing import Dict, List

import pandas as pd

from pandas_utils import read_parquet, save_to_parquet

# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals


def get_raw_masks(
    df,
    tweet_search_terms_list: List[str],
    case_sensitive_tweet_search_terms_list: List[str],
    joined_tweet_search_terms_no_spaces_list: List[str],
) -> List[pd.Series]:
    """Get masks for tweets with types of wanted terms in text."""
    lowercase_mask = (
        df["text"].str.lower().str.contains("|".join(tweet_search_terms_list))
    )
    case_mask = df["text"].str.contains(
        "|".join(case_sensitive_tweet_search_terms_list)
    )
    joined_case_mask = (
        df["text"]
        .str.lower()
        .str.replace(" ", "")
        .str.contains("|".join(joined_tweet_search_terms_no_spaces_list))
    )
    print("Created masks to filter raw data based on wanted text in tweets")
    return [lowercase_mask, case_mask, joined_case_mask]


def add_search_term_boolean_columns(
    df: pd.DataFrame,
    lowercase_mask: pd.Series,
    case_mask: pd.Series,
    joined_case_mask: pd.Series,
    crypto_terms_list: List[str],
    religious_terms_list: List[str],
    inappropriate_terms_list: List[str],
    video_games_terms_list: List[str],
    misc_unwanted_terms_list: List[str],
    non_english_terms_list: List[str],
) -> pd.DataFrame:
    """Add boolean to indicate presence of wanted/unwanted terms in tweet."""
    df = (
        df.assign(contains_wanted_text=lowercase_mask)
        .assign(contains_wanted_text_case_sensitive=case_mask)
        .assign(contains_multi_word_wanted_text=joined_case_mask)
        .assign(
            contains_crypto_terms=df["text"].str.contains(
                "|".join(crypto_terms_list)
            )
        )
        .assign(
            contains_religious_terms=df["text"].str.contains(
                "|".join(religious_terms_list)
            )
        )
        .assign(
            contains_inappropriate_terms=df["text"].str.contains(
                "|".join(inappropriate_terms_list)
            )
        )
        .assign(
            contains_video_games_terms=df["text"].str.contains(
                "|".join(video_games_terms_list)
            )
        )
        .assign(
            contains_misc_unwanted_terms=df["text"].str.contains(
                "|".join(misc_unwanted_terms_list)
            )
        )
        .assign(
            contains_non_english_terms=df["text"].str.contains(
                "|".join(non_english_terms_list)
            )
        )
    )
    print(
        "Created boolean columns to indicate presence of unwanted terms in "
        "tweets"
    )
    terms_str = []
    pcts_total = []
    for c in df.columns[df.columns.str.endswith("_terms")]:
        pct_of_total = (df[c].sum() / len(df)) * 100
        term_type = c.replace("contains_", "").replace("_terms", "")
        term_str = f"{term_type}={pct_of_total:.3f}"
        terms_str.append(term_str)
        pcts_total.append(pct_of_total)
    term_str_full = (
        " | ".join(terms_str) + f" | total unwanted={sum(pcts_total):.3f}"
    )
    print(term_str_full)
    return df


def apply_masks(
    df: pd.DataFrame,
    case_mask: pd.Series,
    lowercase_mask: pd.Series,
    joined_case_mask: pd.Series,
    unwanted_partial_strings_list: List[str],
) -> pd.DataFrame:
    """Apply masks for only keeping tweets based on terms in text."""
    df = df.loc[case_mask].loc[lowercase_mask].loc[joined_case_mask]
    unwanted_mask = df["text"].str.contains(
        "|".join(unwanted_partial_strings_list)
    )
    df = df.loc[~unwanted_mask]
    print(f"Kept {len(df):,} tweets after filtering raw data with masks")
    return df


def filter_by_num_words_in_tweet(
    df: pd.DataFrame, min_num_tweet_words_wanted: int
) -> pd.DataFrame:
    """Filter tweets based on number of words in text."""
    min_num_words_mask = (
        df["text"].str.split(" ").str.len() >= min_num_tweet_words_wanted
    )
    print(
        f"Kept {len(df.loc[min_num_words_mask]):,} tweets with more than "
        f"approximately {min_num_tweet_words_wanted:,} words per tweet"
    )
    df = df.loc[min_num_words_mask]
    return df


def filter_files_per_hour(
    proc_files: List[str],
    tweet_search_terms: List[str],
    case_sensitive_tweet_search_terms: List[str],
    joined_tweet_search_terms_no_spaces: List[str],
    crypto_terms: List[str],
    religious_terms: List[str],
    inappropriate_terms: List[str],
    video_games_terms: List[str],
    misc_unwanted_terms: List[str],
    non_english_terms: List[str],
    unwanted_partial_strings_list: List[str],
    min_num_words_tweet: int,
    dtypes_dict: Dict,
    processed_data_dir: str,
) -> pd.DataFrame:
    """Filter files combined per hour."""
    records = []
    for k, f in enumerate(proc_files, 1):
        start = datetime.now()
        print(
            f"Filtering Tweets from combined data file {k}/ "
            f"{len(proc_files):,} ({os.path.basename(f)})\nStarting time = "
            f"{start.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}..."
        )
        # extract
        df_combined = read_parquet(f, None, None, True)
        # transform
        lowercase_mask, case_mask, joined_case_mask = get_raw_masks(
            df_combined,
            tweet_search_terms,
            case_sensitive_tweet_search_terms,
            joined_tweet_search_terms_no_spaces,
        )
        df_filtered = (
            df_combined.pipe(
                add_search_term_boolean_columns,
                lowercase_mask=lowercase_mask,
                case_mask=case_mask,
                joined_case_mask=joined_case_mask,
                crypto_terms_list=crypto_terms,
                religious_terms_list=religious_terms,
                inappropriate_terms_list=inappropriate_terms,
                video_games_terms_list=video_games_terms,
                misc_unwanted_terms_list=misc_unwanted_terms,
                non_english_terms_list=non_english_terms,
            )
            .pipe(
                apply_masks,
                case_mask=case_mask,
                lowercase_mask=lowercase_mask,
                joined_case_mask=joined_case_mask,
                unwanted_partial_strings_list=unwanted_partial_strings_list,
            )
            .pipe(
                filter_by_num_words_in_tweet,
                min_num_tweet_words_wanted=min_num_words_tweet,
            )
            .astype(dtypes_dict)
        )
        end = datetime.now()
        duration = (end - start).total_seconds()
        print(
            "Done filtering at "
            f"{end.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} ({duration:.3f} "
            "seconds)."
        )
        # load
        file_name = (
            f"filtered__{os.path.basename(f).split('.')[0]}"
            # f"__{end.strftime('%Y%m%d_%H%M%S')}"
        )
        filepath = f"{processed_data_dir}/{file_name}.parquet.gzip"
        save_to_parquet(df_filtered, filepath, None)
        records.append(
            {
                "filename": f,
                "num_rows_combined": len(df_combined),
                "num_rows_filtered": len(df_filtered),
            }
        )
        if k < len(proc_files):
            print()
    # summarize
    df_summary = pd.DataFrame.from_records(records)
    num_combined_rows = df_summary["num_rows_combined"].sum()
    num_filtered_rows = df_summary["num_rows_filtered"].sum()
    print(
        f"\nCombined data contained {num_combined_rows:,} rows\n"
        f"Filtered data contains {num_filtered_rows:,} rows"
    )
    return df_summary
