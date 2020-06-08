# !/usr/bin/env python3

# timesheet.py
# Bix 1/8/19
# get deputy timesheet

import requests, json
import pandas as pd
from pandas.io.json import json_normalize 

date = '2019-01-18'
urls = ['https://numbers.na.deputy.com/api/v1/resource/Timesheet/QUERY',
	'https://numbers.na.deputy.com/api/v1/resource/Timesheet/QUERY']
tokens = ['OAuth token', 
	'OAuth token']
date_json = json.dumps({'search':{'f1':{'field':'Date','data':date,'type':'ge'},
	'f2':{'field':'Date','data':date,'type':'le'}}})
column_keys = ['EndTimeLocalized','StartTimeLocalized', 'TotalTime', 'TotalTimeInv',
	'_DPMetaData.EmployeeInfo.DisplayName', '_DPMetaData.EmployeeInfo.Id',
	'_DPMetaData.OperationalUnitInfo.LabelWithCompany']
dfs = {}
COLUMN_KEYS_TIMESHEET = ['EndTimeLocalized','StartTimeLocalized','TotalTime', 
	'TotalTimeInv','_DPMetaData.EmployeeInfo.DisplayName',
	'_DPMetaData.EmployeeInfo.Id','_DPMetaData.OperationalUnitInfo.LabelWithCompany']
	
for i in range(len(urls)):
	response = requests.post(urls[i], date_json, headers={'Authorization':tokens[i]})
	if response.status_code == requests.codes.ok:
		response_json = response.json()
		# print(json.dumps(response_json, sort_keys=True, indent=4, separators=(',', ': ')))
		df = json_normalize(response_json)
		# print(df.keys())
		df = df.loc[:,column_keys]
		dfs[i]=df
	else:
		response.raise_for_status()

df_combined = dfs[0]		
for k in dfs.keys():
	if k != 0:
		df_combined = df_combined.append(dfs[k], ignore_index=True)
df_combined.to_csv("timesheet.csv")
print('CSV Created')