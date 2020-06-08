# !/usr/bin/env python3

# vehicle_settings.py
# Bix 1/24/19
# vehicle_settings for workwave 

import json

class VehicleSettings:
	"""VehicleSettings Class for WorkWave"""

	def __init__(self):
		self.data = {}
		self.data["available"]="true"
		self.data["notes"]="vehicle set via api"

	def create_json(self):
		try:
			json_data = json.dumps(self.data)
			print(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))

		except Exception as e:
			print('VS_create_json',e)

if __name__ == '__main__':
	# vs1 = vehicle_settings.VehicleSettings()
	vs1 = VehicleSettings()
	vs1.create_json()