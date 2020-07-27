#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import agg
import unittest


class AggTest(unittest.TestCase):

    def test_merge_csv(self):

        # input file does not exist:
        self.assertRaises(
            FileNotFoundError,
            agg.merge_csv,
            ('testfiles/file_01.csv', 'testfiles/file_02.csv', 'notThere.csv'),
            'test_output.csv',
            True)

        # folder for output file does not exist:
        self.assertRaises(
            ValueError,
            agg.merge_csv,
            ('testfiles/file_01.csv', 'testfiles/file_02csv.', 'notThere.csv'),
            '/non-existent/test_output.csv',
            True)


if __name__ == "__main__":
    unittest.main()
