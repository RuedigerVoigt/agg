#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Agg
~~~~~~~~~~~~~~~~~~~~~
Agg aggregates files / data. This initial version only
supports merging CSV files-
"""

# python standard library:
import csv
import gc
import logging
import os
import pathlib
import shutil
import tempfile
from typing import Union, Optional

# 3rd party
import userprovided


def merge_csv(files_to_merge: tuple,
              output_file: Union[str, pathlib.Path],
              first_line_is_header: Optional[bool] = None) -> dict:
    """Merges multiple CSV files in the order they are specified.
       This will overwrite any existing file with the same name.

    Args:
        files_to_merge: A tuple containing paths to a files in the order
            they are to be merged.
        output_file: The path to the result file. The folder must already
            exist. An existing file with the same name will be overwritten.
        first_line_is_header: optional; if True agg will remove the first
            line of all csv files except for the first. If not set agg will
            guess if the first line is a header or not.

    Returns:
        A dictionary containing:
            * a SHA256 hash of the result file,
            * its absolute path,
            * its size in bytes.
        E.g.:
        {'sha256hash': 'fff30942d3d042c5128062d1a29b2c50494c3d1d033749a58268d2e687fc98c6',
         'file_path': '/home/exampleuser/merged_file',
         'file_size_bytes': 76}

    Raises:
        ValueError: If the folder for the target file does not exist.
        FileNotFoundError: If one of the specified files does not exist.
    """

    # ############## Check Path ##############

    if not pathlib.Path(output_file).parent.exists():
        raise ValueError("Specified folder does not exist. " +
                         "Cannot create file.")

    # ############## Check Header ##############

    if first_line_is_header is None:
        # The user did not specify if the file has a header.
        # Read the first file into RAM:
        with open(files_to_merge[0], 'r', newline='') as file:
            first_file_ram = file.read()
        first_line_is_header = csv.Sniffer().has_header(first_file_ram)
        if first_line_is_header:
            logging.debug('Detected first line is a header.')
        else:
            logging.debug("Detected first line is *not* a header.")
        # The file might be huge. So explicitly free the memory
        del first_file_ram
        gc.collect()

    # ############## Merge Files ##############

    try:
        # Do NOT use tempfile.NamedTemporaryFile as it is platform dependent
        # whether you can read the file while it is open and it will be
        # deleted as soon it is closed.
        temp_handle, temp_path = tempfile.mkstemp()

        with open(temp_path, 'w') as temp_out:
            csvwrt = csv.writer(temp_out)
            for i, csvfile in enumerate(files_to_merge):
                with open(csvfile, 'r', newline='') as in_file:
                    csvrdr = csv.reader(in_file)
                    if i != 0 and first_line_is_header:
                        # Not the first line and the files contain headers.
                        # => Skip the first line by incrementing the iterator
                        next(csvrdr)
                    for line in csvrdr:
                        # Using csv.writerow ensures that linebreaks are added
                        # even if the last line of a file did not have one.
                        csvwrt.writerow(line)
        try:
            # https://github.com/python/mypy/issues/7082 :
            shutil.copyfile(temp_path, output_file, follow_symlinks=True)  # type: ignore
            logging.info("Succesfully written file")
        except Exception:
            logging.exception("Failed to copy temp file into target path!")
            raise

    except FileNotFoundError:
        logging.exception("File Not Found: Could not complete the merge." +
                          "Some of the specified files is missing or not " +
                          "readable.")
        raise
    finally:
        # mkstemp() requires to explicitly delete the filehandle and file
        os.close(temp_handle)
        os.remove(temp_path)
        gc.collect()

    result = dict()
    result['sha256hash'] = userprovided.hash.calculate_file_hash(
        pathlib.Path(output_file), 'sha256')

    # The format of the absolute path is dependent on the OS, but
    # pathlib.Path() automatically takes care of that:
    full_path = str(pathlib.Path(output_file).resolve())
    result['file_path'] = full_path

    # assigning an int causes a mypy error because other values were string
    result['file_size_bytes'] = pathlib.Path(output_file).stat().st_size  # type: ignore

    return result
