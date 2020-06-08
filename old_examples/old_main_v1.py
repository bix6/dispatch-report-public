#!/usr/bin/env python3

# main.py
# Bix 1/8/19
# dispatch report main

import requests, json
import pandas as pd

url = 'https://numbers.na.deputy.com/api/v1/resource/Timesheet/QUERY'

date = json.dumps({'search':{'f1':
{'field':'Date','data':'2018-12-24','type':'ge'},
'f2':{'field':'Date','data':'2018-12-24','type':'le'}}})

r1 = requests.post(url, date, headers={'Authorization':'OAuth token'})

if r1.status_code == requests.codes.ok:
	r1json = r1.json()
	print('\n\n\nReturned JSON\n\n\n')
	print(json.dumps(r1json, sort_keys=True, indent=4, separators=(',', ': ')))
	df = pd.DataFrame(r1json)
	df.to_csv("r1json.csv")
	print('\nCSV Created\n')

else:
	r1.raise_for_status()