# Changelog for agg

## UPCOMING 0.4.0

* Fix bug #1: You now can set the linebreak used in the merged file explicitly. In case you do not set this parameter, the standard linebreaks of your operating system will be used.
* Update dependency `userprovided`.
* Report test coverage.

## Version 0.3.1

* Switch from unittest to pytest and increase test coverage.
* Updated dependencies.
* Found bug #1 in the Windows version. (Not fixed in this release.)

## Version 0.3.0

* Test with Python 3.9.
* Mark library as stable.
* Return dictionary now also contains the file name.

## Version 0.2.0

* The method `merge_csv` now returns a dictionary with information about the just created file.

## Version 0.1.0

* `merge_csv`: merge two or more CSV files