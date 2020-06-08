# !/usr/bin/env python3

# requester.py
# Bix 1/23/19
# access apis and return json data in pandas dataframe

import requests
from pandas.io.json import json_normalize 

def get_json(url_in,headers_in,date_in=None,column_keys_in=None):
	if date_in != None:
		response = requests.post(url_in, date_in, headers=headers_in)
	else:
		response = requests.get(url_in, headers=headers_in)

	if response.status_code == requests.codes.ok:
		response_json = response.json()
		df = json_normalize(response_json)
		if column_keys_in != None:
			df = df.loc[:,column_keys_in]
		return df
	else:
		response.raise_for_status()

