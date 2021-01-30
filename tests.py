#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Automatic Tests for agg

To run these tests:
coverage run --source agg -m pytest tests.py
To generate a report afterwards.
coverage html
~~~~~~~~~~~~~~~~~~~~~
Source: https://github.com/RuedigerVoigt/agg
(c) 2020-2021 Rüdiger Voigt
Released under the Apache License 2.0
"""

import pytest
import agg


def test_missing_input_file():
    with pytest.raises(FileNotFoundError):
        agg.merge_csv(
            ('testfiles/file_01.csv', 'notThere.csv'),
            'test_output.csv',
            False)
    with pytest.raises(FileNotFoundError):
        agg.merge_csv(
            ('testfiles/file_01.csv', 'testfiles/file_02.csv', 'notThere.csv'),
            'test_output.csv',
            False)


def test_missing_folder_for_output():
    with pytest.raises(ValueError):
        agg.merge_csv(
            ('testfiles/file_01.csv', 'testfiles/file_01.csv'),
            'non_existent_folder/test_output.csv',
            True)


def test_return_value():
    result = agg.merge_csv(
        ('testfiles/file_01.csv', 'testfiles/file_02.csv'),
        'combined_file.csv',
        True)
    #assert result['sha256hash'] == 'fff30942d3d042c5128062d1a29b2c50494c3d1d033749a58268d2e687fc98c6'
    assert result['file_name'] == 'combined_file.csv'
    # not tested result['file_path'] because system dependent
    assert result['first_line_is_header'] is True
    #assert result['file_size_bytes'] == 76
    #assert result['line_count'] == 8
    # Paths depend on the system, but count elements:
    assert len(result['merged_files']) == 2


def test_no_info_about_header():
    result = agg.merge_csv(
        ('testfiles/file_01.csv', 'testfiles/file_02.csv'),
        'combined_file_with_header.csv',
        None)
    assert result['first_line_is_header'] is True
    result = agg.merge_csv(
        ('testfiles/no_header_01.csv', 'testfiles/no_header_02.csv'),
        'combined_file_wo_header.csv',
        None)
    assert result['first_line_is_header'] is False
