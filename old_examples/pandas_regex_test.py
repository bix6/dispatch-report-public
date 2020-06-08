# !/usr/bin/env python3

# pandas_test_regex.py
# Bix 1/23/19
# pandas testing regex

import pandas as pd

DATE = '2019-01-23'
my_df = pd.read_csv('output/rfv_merged.csv')
print(my_df.head())
print(type(my_df))
my_df = my_df.loc[:,'StartTimeLocalized']
print(my_df.head())
print(type(my_df))
rgx = r'(\d*-\d*-\d*)(\w)(\d*:\d*:\d*)(-)(\d*:\d*)'
my_df = pd.Series(my_df).str.replace(rgx,r'\3',regex=True)
print(my_df.head())
print(type(my_df))