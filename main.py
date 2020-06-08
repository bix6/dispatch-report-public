# !/usr/bin/env python3

# main.py
# Bix 1/31/19
# main

import datetime
import modules.config as config
import modules.quickstart as quickstart
import modules.driver as driver
import csv

GET_DATA = True
# GET_DATA = False
MAKE_REPORT = True
# MAKE_REPORT = False
DATE_NOW = datetime.datetime.now().strftime("%Y-%m-%d")
# DATE_NOW = "2019-02-17"
# DATE_NOW = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")


print('Starting...')
if GET_DATA:
	print('Getting Data...')
	my_config = config.Config(DATE_NOW)
	my_config.main()
	my_quickstart = quickstart.Quickstart(DATE_NOW)
	my_quickstart.main()
	print('CSVs Created')
if MAKE_REPORT:
	print('Creating Reports...')
	with open('output/'+DATE_NOW+'_rfv-merged-rgx.csv') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',',quotechar='|')
		rows=[]
		for row in csv_reader:
			if len(row)==7: # need a better check
				rows.append(row)
			else:
				print('skipping row: ',row)
	my_drivers = []
	for r in rows[1:]:
		my_drivers.append(driver.Driver(r))
	my_drivers[0].create_report(my_drivers[0].DAY_SHIFT)
	my_drivers[0].create_report(my_drivers[0].NIGHT_SHIFT,day_shift_in=False)
	print('Reports Created')
print('Done')