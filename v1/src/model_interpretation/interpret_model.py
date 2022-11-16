#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Utilities to help interpret a trained ML model."""


from typing import List

from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame as pdf

# pylint: disable=invalid-name,eval-used


def get_term(row, vocabulary_list: List[str]) -> List[str]:
    """Get a term, based on its index, from a text vocabulary."""
    index = row["termIndices"]
    terms = [vocabulary_list[t] for t in index]
    return terms


def ith_(v, i: int) -> float:
    """Get value based on its index in an array-like structure."""
    try:
        return float(v[i])
    except ValueError:
        return None


def get_max_val_name(
    df: pdf, cols_to_use: List[str], new_col_names: List[str]
) -> pdf:
    """Get max value and its column name, from subset of columns, per row."""
    cond = "F.when" + ".when".join(
        [
            "(F.col('" + c + "') == F.col('max_value'), F.lit('" + c + "'))"
            for c in cols_to_use
        ]
    )
    df_with_max_value_name = df.withColumn(
        "max_value", F.greatest(*cols_to_use)
    ).withColumn("MAX", eval(cond))
    for old, new in zip(["max_value", "MAX"], new_col_names):
        df_with_max_value_name = df_with_max_value_name.withColumnRenamed(
            old, new
        )
    return df_with_max_value_name
