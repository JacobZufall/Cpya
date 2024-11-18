# PyActy

A library containing functions used in various branches of accounting.

The idea of this library is to introduce Python to the accounting industry. For example, and auditor could use this
library to perform test of details, or a tax accountant could use it to calculate an itemized deduction. This library is
still in its infancy, so most potential uses are yet to emerge.

## Disclaimer

I am a self-taught programmer, and this project is mainly intended to be a teaching tool for me, since I learn by doing.
Because of this, this package may have many mistakes and questionable practices.


## Version Format

All releases will be tagged as v[YYYY].[MM].[DD]-rV.

- YYYY is the latest fiscal year the version is usable in.
- MM is the month the version was released in.
- DD is the day the version was released in.
- V is the revision, or number of releases made, for that day. This helps in the case that multiple versions occur on 
the same day.

In the event that the changes related to the tax functions aren't useable in the currently fiscal year, every update 
should be marked as v2023.12.31-r[V].
