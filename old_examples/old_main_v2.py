# !/usr/bin/env python3

# main.py
# Bix 1/23/19
# main

import requester, json
import pandas as pd
import yaml
import datetime

print('Running...')

OUTPUT_PATH = 'output/'
DATE = datetime.datetime.now().strftime("%Y-%m-%d")
DATE_PLUS1 = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
# DATE = '2019-02-01'
DATE_JSON = json.dumps({'search':{'f1':{'field':'Date','data':DATE,'type':'ge'},
	'f2':{'field':'Date','data':DATE,'type':'le'}}})
DATES = [DATE_JSON,DATE_JSON,None,None]

CONF_PATH='config/config_apis.yml'
URLS=[]
HEADERS_AUTH=[]
with open(CONF_PATH, 'r') as f:
    conf = yaml.safe_load(f)
    for i in range(len(conf['urls'])):
    	URLS.append(conf['urls'][i])
    	HEADERS_AUTH.append(conf['headers'][i])

COLUMN_KEYS_ROSTER = ['Comment','EndTimeLocalized','StartTimeLocalized',
	'_DPMetaData.EmployeeInfo.DisplayName',
	'_DPMetaData.OperationalUnitInfo.LabelWithCompany']
COLUMN_KEYS_FLEETIO = ['contact_full_name','ended_at','started_at','vehicle_id']
COLUMN_KEYS_VEHICLES = ['id','name']
COLUMN_KEYS = [COLUMN_KEYS_ROSTER,COLUMN_KEYS_ROSTER,COLUMN_KEYS_FLEETIO,
	COLUMN_KEYS_VEHICLES]
COLUMN_KEYS_FINAL = ['contact_full_name','name','StartTimeLocalized',
	'EndTimeLocalized','_DPMetaData.OperationalUnitInfo.LabelWithCompany','Comment']


dfs = {}

for i in range(len(my_config.URLS)):
	dfs[i] = requester.get_json(url_in=URLS[i],headers_in=HEADERS_AUTH[i],
		date_in=DATES[i],column_keys_in=COLUMN_KEYS[i])
df_roster = dfs[0].append(dfs[1],ignore_index=True)
df_fleetio = dfs[2]
df_vehicles = dfs[3]

dfs[0].append(dfs[1],ignore_index=True).to_csv(OUTPUT_PATH+"roster.csv")
dfs[2].to_csv(OUTPUT_PATH+"fleetio.csv")
dfs[3].to_csv(OUTPUT_PATH+"vehicles.csv")

df_fleetio = df_fleetio[df_fleetio.started_at.str[0:10]==DATE]
df_vehicles = df_vehicles.rename(index=str, columns={"id": "vehicle_id"})
df_fv_merged = pd.merge(df_fleetio, df_vehicles, on="vehicle_id")
df_fv_merged.to_csv("output/fv_merged.csv")

df_roster = df_roster.rename(index=str, 
	columns={"_DPMetaData.EmployeeInfo.DisplayName": "contact_full_name"})
df_rfv_merged = pd.merge(df_roster, df_fv_merged, on="contact_full_name", how="outer")
df_rfv_merged = df_rfv_merged.loc[:,COLUMN_KEYS_FINAL]
df_rfv_merged = df_rfv_merged.rename(index=str, columns={"contact_full_name": "Name",
		"name":"Truck",
		"_DPMetaData.OperationalUnitInfo.LabelWithCompany":"Role"})

df_rfv_merged.to_csv("output/rfv_vehicle_settings_in.csv")

rgx = r'(\d*-\d*-\d*)(\w)(\d*:\d*:\d*)(-)(\d*:\d*)'
for t in ['StartTimeLocalized','EndTimeLocalized']:
	series_t = df_rfv_merged.loc[:,t]
	series_t = pd.Series(series_t).str.replace(rgx,r'\3',regex=True)
	df_rfv_merged[t]=series_t

df_rfv_merged.to_csv("output/rfv_merged"+DATE+".csv")
print('CSVs created')