# !/usr/bin/env python3

# config.py
# Bix 1/24/19
# config

import json, yaml, requests
import pandas as pd
from pandas.io.json import json_normalize

class Config:
	"""Config Class"""

	def __init__(self, date_in):
		self.OUTPUT_PATH = 'output/'
		self.DATE_NOW = date_in
		self.DATE_NOW_JSON = json.dumps({'search':{'f1':{'field':'Date',
			'data':self.DATE_NOW,'type':'ge'},'f2':{'field':'Date',
			'data':self.DATE_NOW,'type':'le'}}})
		self.DATES = [self.DATE_NOW_JSON,self.DATE_NOW_JSON,None,None]

		self.CONF_PATH = 'config/config_apis.yml'
		self.URLS=[]
		self.HEADERS_AUTH=[]
		with open(self.CONF_PATH, 'r') as f:
			conf = yaml.safe_load(f)
			for i in range(len(conf['urls'])):
				self.URLS.append(conf['urls'][i])
				self.HEADERS_AUTH.append(conf['headers'][i])

		self.COLUMN_KEYS_ROSTER = ['Comment','EndTimeLocalized',
			'StartTimeLocalized','_DPMetaData.EmployeeInfo.DisplayName',
			'_DPMetaData.OperationalUnitInfo.LabelWithCompany']
		self.COLUMN_KEYS_FLEETIO = ['contact_full_name','ended_at','started_at',
			'vehicle_id']
		self.COLUMN_KEYS_VEHICLES = ['id','name']
		self.COLUMN_KEYS = [self.COLUMN_KEYS_ROSTER,self.COLUMN_KEYS_ROSTER,
			self.COLUMN_KEYS_FLEETIO,self.COLUMN_KEYS_VEHICLES]
		self.COLUMN_KEYS_FINAL = ['contact_full_name','name','StartTimeLocalized',
			'EndTimeLocalized','_DPMetaData.OperationalUnitInfo.LabelWithCompany',
			'Comment']
		self.dfs = {} 

	def get_json(self, url_in,headers_in,date_in=None,column_keys_in=None):
		if date_in != None:
			response = requests.post(url_in, date_in, headers=headers_in)
		else:
			response = requests.get(url_in, headers=headers_in)

		if response.status_code == requests.codes.ok:
			response_json = response.json()
			df_response = json_normalize(response_json)
			if column_keys_in != None:
				df_response = df_response.loc[:,column_keys_in]
			return df_response
		else:
			response.raise_for_status()

	def df_to_csv(self, df_in, str_in):
		str_start = self.OUTPUT_PATH + self.DATE_NOW + "_"
		str_end = ".csv"
		if isinstance(df_in, list):
			for i in range(len(df_in)):
				df_in[i].to_csv(str_start + str_in[i] + str_end)
		elif isinstance(str_in, str):
			df_in.to_csv(str_start + str_in + str_end)

	def get_data_frames(self):
		for i in range(len(self.URLS)):
			self.dfs[i] = self.get_json(url_in=self.URLS[i],
				headers_in=self.HEADERS_AUTH[i],date_in=self.DATES[i],
				column_keys_in=self.COLUMN_KEYS[i])
		self.df_roster = self.dfs[0].append(self.dfs[1],ignore_index=True)
		self.df_fleetio = self.dfs[2]
		self.df_vehicles = self.dfs[3]

		self.df_to_csv([self.df_roster,self.df_fleetio,self.df_vehicles],
			["roster","fleetio","vehicles"])

	def manipulate_data_frames(self):
		self.df_fleetio = self.df_fleetio[self.df_fleetio.started_at.str[0:10]==self.DATE_NOW]
		self.df_vehicles = self.df_vehicles.rename(index=str, columns={"id": "vehicle_id"})
		self.df_fv_merged = pd.merge(self.df_fleetio, self.df_vehicles, on="vehicle_id")

		self.df_roster = self.df_roster.rename(index=str, 
			columns={"_DPMetaData.EmployeeInfo.DisplayName": "contact_full_name"})
		self.df_rfv_merged = pd.merge(self.df_roster, self.df_fv_merged, on="contact_full_name", how="outer")
		self.df_rfv_merged = self.df_rfv_merged.loc[:,self.COLUMN_KEYS_FINAL]
		self.df_rfv_merged = self.df_rfv_merged.rename(index=str, columns={"contact_full_name": "Name",
				"name":"Truck",
				"_DPMetaData.OperationalUnitInfo.LabelWithCompany":"Role"})
		self.df_to_csv([self.df_fv_merged, self.df_rfv_merged],
			["fv-merged","rfv-merged"])

		rgx = r'(\d*-\d*-\d*)(\w)(\d*:\d*:\d*)(-)(\d*:\d*)'
		for t in ['StartTimeLocalized','EndTimeLocalized']:
			series_t = self.df_rfv_merged.loc[:,t]
			series_t = pd.Series(series_t).str.replace(rgx,r'\3',regex=True)
			self.df_rfv_merged[t]=series_t
		self.df_to_csv(self.df_rfv_merged,"rfv-merged-rgx")

	def main(self):
		self.get_data_frames()
		self.manipulate_data_frames()

