#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import agg

# tuples are ordered:
my_files = ('testfiles/file_01.csv', 'testfiles/file_02.csv')

# Merge the CSV-files - in the specified order - into a new file called
# "merged_file". Meanwhile copy the header / first line only once from
# first file
file_data = agg.merge_csv(my_files, 'merged_file', True)

# The method returned a dictionary with some information
# about the output file:
print(file_data)

print(file_data['file_path'])
