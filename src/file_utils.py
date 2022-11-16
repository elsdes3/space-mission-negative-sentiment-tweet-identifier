#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""File handling utilities."""


import os
import zipfile
from glob import glob

# pylint: disable=invalid-name
# pylint: disable=too-many-arguments


def create_zip_file_from_folder(
    processed_data_dir: str, zip_fname: str, filepath: str
) -> None:
    """Create zipped file from contents of a folder."""
    # create a ZipFile object
    zip_fpath = os.path.join(processed_data_dir, zip_fname)
    if not os.path.exists(zip_fpath):
        with zipfile.ZipFile(zip_fpath, "w") as zipObj:
            # Iterate over all the files in directory
            for folderName, _, filenames in os.walk(filepath):
                for filename in filenames:
                    # print(folderName, filename)
                    # create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # # Add file to zip
                    zipObj.write(filePath, os.path.basename(filePath))


def create_zip_file(
    file_search_pattern_str: str,
    processed_data_dir: str,
    proc_data_zip_fname: str,
):
    """Create zipped file."""
    os.chdir(processed_data_dir)
    if not os.path.exists(proc_data_zip_fname):
        ZipFile = zipfile.ZipFile(proc_data_zip_fname, "w")
        for f in glob(file_search_pattern_str):
            ZipFile.write(f, compress_type=zipfile.ZIP_DEFLATED)
        ZipFile.close()
        processed_data_fpath = os.path.join(
            processed_data_dir, proc_data_zip_fname
        )
        print(f"Created zip file at {processed_data_fpath}")
    os.chdir("../../")
    os.chdir("notebooks")
