# !/usr/bin/env python3

# pandas_test.py
# Bix 1/23/19
# pandas testing merges

import pandas as pd

DATE = '2019-01-23'
df_fleetio = pd.read_csv('output/fleetio.csv')
# df_fleetio = df_fleetio.loc[df_fleetio['current']==True]
df_fleetio = df_fleetio[df_fleetio.started_at.str[0:10]==DATE]
df_fleetio.to_csv("output/m1.csv")
df_vehicles = pd.read_csv('output/vehicles.csv')
df_vehicles = df_vehicles.rename(index=str, columns={"id": "vehicle_id"})
print(df_fleetio.head())
print(df_vehicles.head())
df_merged = pd.merge(df_fleetio, df_vehicles, on="vehicle_id")
df_merged.to_csv("output/merged.csv")
print(df_merged.head())

df_roster = pd.read_csv('output/roster.csv')
df_roster = df_roster.rename(index=str, 
	columns={"_DPMetaData.EmployeeInfo.DisplayName": "contact_full_name"})
df_new2 = pd.merge(df_roster, df_merged, on="contact_full_name", how="outer")
df_new2.to_csv("output/merged2.csv")
