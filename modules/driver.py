# !/usr/bin/env python3

# driver.py
# Bix 2/1/19
# driver

import re, datetime

class Driver:
	"""Driver Class"""
	DRIVER_LOCS_DAY = {}
	DRIVER_LOCS_NIGHT = {}
	DAY_SHIFT = []
	NIGHT_SHIFT = []

	def __init__(self, info_in):
		print(info_in)
		self.NAME = info_in[1]
		self.TRUCK = info_in[2].title()
		self.START = info_in[3]
		self.END = info_in[4]
		self.ROLE = info_in[5]
		self.NOTES = info_in[6]
		self.LEAD = False
		self.DISPATCHER = False
		self.DRIVER = False
		self.LOC = None
		self.SHIFT = 'DAY'

		if self.NAME in ['Lead Driver Name', 'Lead Driver Name','Lead Driver Name','Lead Driver Name']:
			self.LEAD = True
		elif self.NAME in ['Dispatcher Name', 'Dispatcher Name' ,'Dispatcher Name','Dispatcher Name','Dispatcher Name']:
			self.DISPATCHER = True
		else:
			self.DRIVER = True

		if int(self.START[:self.START.index(':')]) > 12:
			self.SHIFT = 'NIGHT'
			Driver.NIGHT_SHIFT.append(self)
		else:
			Driver.DAY_SHIFT.append(self)

		rgx = re.compile(r'\[(\w{3})\]')
		search = rgx.search(self.ROLE)
		if search:
			self.LOC = search.group(1)
			if self.SHIFT == 'DAY':
				Driver.DRIVER_LOCS_DAY.setdefault(self.LOC, []).append(self.NAME)
			else:
				Driver.DRIVER_LOCS_NIGHT.setdefault(self.LOC, []).append(self.NAME)
		print()	
		# print(info_in)
		# print(self.LEAD,self.DISPATCHER,self.DRIVER)
		# print(self.LOC)
		# print(Driver.DRIVER_LOCS)
		print()
		self.create_str()


	def create_str(self):
		info_str = ''
		NAME_STR = '<b><u>'+self.NAME+'</b></u> - '
		NAME_STR_INFO = '<b><u>'+self.NAME+'</b></u> -<br><b>Info:</b> '
		FILLS_STR = '<br><b>Fills:</b><br><b>Hours:</b><br><b>FPH:</b><br>'
		if self.LEAD:
			if self.TRUCK == '':
				info_str = NAME_STR_INFO+self.START+' - '+self.END+' - '+self.NOTES+'<br>'
			else:
				if self.NOTES == '':
					info_str = NAME_STR_INFO+self.START+' - '+self.END+' - '+self.TRUCK+FILLS_STR
				else:
					info_str = NAME_STR_INFO+self.START+' - '+self.END+' - '+self.TRUCK+' - '+self.NOTES+FILLS_STR
		elif self.DISPATCHER:
			if self.NOTES == '':
				info_str = NAME_STR+self.START+' - '+self.END
			else:
				info_str = NAME_STR+self.START+' - '+self.END+' - '+self.NOTES
		else:
			if self.NOTES == '':
				if self.TRUCK == '':
					info_str = NAME_STR_INFO+self.START+' - '+self.END+FILLS_STR
				else:
					info_str = NAME_STR_INFO+self.START+' - '+self.END+' - '+self.TRUCK+FILLS_STR
			else:
				if self.TRUCK == '':
					info_str = NAME_STR_INFO+self.START+' - '+self.END+' - '+self.NOTES+FILLS_STR
				else:
					info_str = NAME_STR_INFO+self.START+' - '+self.END+' - '+self.TRUCK+' - '+self.NOTES+FILLS_STR

		self.INFO_STR = info_str
		print(self.INFO_STR)

	def create_report(self, list_in, day_shift_in=True):
		OUTPUT_LOC = 'output/'
		DATE_NOW = datetime.datetime.now().strftime("%m/%d/%Y")
		report_str = ''
		report_str = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Dispatch Report - '+DATE_NOW+'</title></head><body>'
		if day_shift_in == False:
			report_str += 'Location Evening Filld Report for CompanyName -<br><b>Assigned:</b><br><b>Filled:</b><br><b>Notes:</b><br><br>_______________________________<br><br>'
		report_str += '<b>Dispatch Report</b> - All Markets<br><b>Prepared by:</b><br><b>Completed by:</b><br>'
		driver_str = ''
		loc_str = {'DIS':'DISPATCH','VAN':'VANCOUVER','POR':'PORTLAND',
			'MTV':'BAY AREA','WDC':'DC'}
		for k in ['DIS','VAN','POR','MTV','WDC']:
			driver_str += '_______________________________<br><br>'
			driver_str += '<b><i>'+loc_str[k]+'</b></i><br><br>'
			if k == 'VAN':
				driver_str += '<b><u>Totals</b></u><br><b>Evo:</b><br><b>Car2Go:</b><br><br>'
			for i in range(len(list_in)):
				if list_in[i].LOC == k:
					driver_str += list_in[i].INFO_STR+'<br>'
		report_str += driver_str + '</body></html>'
		print(report_str)
		if day_shift_in:
			with open(OUTPUT_LOC+'day.html', 'w') as f:
				f.write(report_str)
		else:
			with open(OUTPUT_LOC+'night.html', 'w') as f:
				f.write(report_str)

