# !/usr/bin/env python3

# pandas_vehicle_settings_experiment
# Bix 1/23/19
# pandas testing merges

import pandas as pd

df_rfv = pd.read_csv("output/rfv_vehicle_settings_in.csv")
df_trucks=df_rfv.dropna(subset=['Truck'])
df_trucks.to_csv("output/TrucksOnly.csv")
print(df_trucks.head())
print(len(df_trucks.index))
df_trucks.loc[:,'Shift'] = 'DAY'
INDEX_LEN = len(df_trucks.index)
INDEX_START = 3
INDEX_END = 4
STRP_CHARS = -6
CUTOFF_HOUR = 12
for r in range(INDEX_LEN):
	ts_start = pd.to_datetime(df_trucks.iloc[r,INDEX_START][:STRP_CHARS],format='%Y-%m-%dT%H:%M:%S')
	ts_end = pd.to_datetime(df_trucks.iloc[r,INDEX_END][:STRP_CHARS],format='%Y-%m-%dT%H:%M:%S')
	if ts_start.hour > CUTOFF_HOUR:
		df_trucks.iat[r,len(df_trucks.columns)-1] = 'NIGHT'
	print(ts_end-ts_start)
	seconds=(ts_end-ts_start).total_seconds()
	hours=seconds/3600
	MIDNIGHT=str(ts_start.year)+'-'+str(ts_start.month)+'-'+str(ts_start.day)+'-0:0:0'
	ssm_ts_start=(ts_start-pd.to_datetime(MIDNIGHT)).total_seconds()
	ssm_ts_end=(ts_end-pd.to_datetime(MIDNIGHT)).total_seconds()
	print(ssm_ts_start)
	print(hours, seconds)
	print(df_trucks.iloc[r,:])
	breaks=[]
	if hours > 2:
		breaks.append({"durationSec":600,"startSec":ssm_ts_start,
			"endSec":ssm_ts_start+5400})
	if hours > 5:
		breaks.append({"durationSec":1800,"startSec":breaks[0]["endSec"]+1800,
			"endSec":breaks[0]["endSec"]+1800+16200})
	if hours > 8:
		breaks.append({"durationSec":600,"startSec":breaks[1]["endSec"]+3600,
			"endSec":ssm_ts_end})
	print(breaks)
	df_breaks = pd.DataFrame(breaks)
	print(df_breaks.head())	

	print('\n\n')
df_trucks.to_csv("output/TrucksOnly2.csv")