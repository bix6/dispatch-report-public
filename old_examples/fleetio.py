# !/usr/bin/env python3

# fleetio.py
# Bix 1/23/19
# get fleetio trucks

import requests, json
import pandas as pd
from pandas.io.json import json_normalize 

url = 'https://secure.fleetio.com/api/v1/vehicles'
headers_fleetio = {'Authorization':'Token Token',
	'Account-Token':'Token'}
column_keys = ['id','name']
response = requests.get(url, headers=headers_fleetio)
if response.status_code == requests.codes.ok:
	response_json = response.json()
	# print(json.dumps(response_json, sort_keys=True, indent=4, separators=(',', ': ')))
	df = json_normalize(response_json)
	print(df.keys())
	df = df.loc[:,column_keys]
	df.to_csv("output/vehicles.csv")
	print('CSV Created')
else:
	response.raise_for_status()