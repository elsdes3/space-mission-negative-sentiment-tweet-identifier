#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Utility functions for notebooks and standalone scripts."""


from IPython.display import display

# pylint: disable=invalid-name


def show_df(df, nrows=5, header=None):
    """Show a few of the first and last rows of a DataFrame."""
    df_slice = df.head(nrows).append(df.tail(nrows)) if nrows else df
    if not header:
        header = f"First & Last {nrows} rows" if nrows else "All rows"
    display(df_slice.style.set_caption(header))


def show_df_dtypes_nans(df):
    """Show datatypes and number of missing rows in DataFrame."""
    display(
        df.isna()
        .sum()
        .rename("num_missing")
        .to_frame()
        .merge(
            df.dtypes.rename("dtype").to_frame(),
            left_index=True,
            right_index=True,
            how="left",
        )
        .style.set_caption("Column Datatypes and Missing Values")
    )


def save_to_parquet_file(dfs, parquet_filepaths):
    """Save DataFrame to parquet file."""
    for parquet_filepath, df in zip(parquet_filepaths, dfs):
        try:
            print(f"Saving data to {parquet_filepath + '.gzip'}", end="...")
            df.to_parquet(
                parquet_filepath + ".gzip",
                engine="auto",
                index=False,
                compression="gzip",
            )
            print("done.")
        except Exception as e:
            print(str(e))
            raise


def summarize_df(df, col_dtype_to_show):
    if col_dtype_to_show == "object":
        # Get string dtype columns
        cols_to_show = list(df.select_dtypes("object"))
        # Get max length of string
        df_max = (
            df[cols_to_show]
            .astype(str)
            .apply(lambda x: x.str.len().max(), axis=0)
            .rename("max_length")
            .to_frame()
        )
    else:
        # Get non-string (numerical) dtype columns
        cols_to_show = list(
            set(list(df)) - set(list(df.select_dtypes("object")))
        )
        # Get max numerical value
        df_max = df[cols_to_show].max().rename("max_value").to_frame()
    display(
        df_max.merge(
            df[cols_to_show].dtypes.rename("dtype").to_frame(),
            left_index=True,
            right_index=True,
            how="left",
        )
        .merge(
            df[cols_to_show].isna().sum().rename("num_missing").to_frame(),
            left_index=True,
            right_index=True,
            how="left",
        )
        .merge(
            df[cols_to_show]
            .dropna(how="any")
            .sample(1)
            .squeeze()
            .rename("single_non_nan_value")
            .to_frame(),
            left_index=True,
            right_index=True,
            how="left",
        )
    )
