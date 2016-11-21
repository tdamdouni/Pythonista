# https://forum.omz-software.com/topic/3179/capture-specific-webpage-text-using-regex-searchhtml-and-save-as-new-textile/7

# https://www.publicapis.com/

import json, requests

def get_json_data(url):
	r = requests.get(url)
	print('r == ', r)
	
	if r.status_code == 200:
		return r.json()
		
if __name__ == '__main__':
	#url = 'https://raw.githubusercontent.com/teelaunch/pms-pantone-color-chart/master/params.json'
	url = 'http://ergast.com/api/f1/2016/drivers.json'
	r = get_json_data(url)
	drivers =  r['MRData']['DriverTable']['Drivers']
	print(drivers)

