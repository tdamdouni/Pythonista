from __future__ import print_function
import os,sys
import requests

def is_pythonista():
	if 'Pythonista' in sys.executable:
		return True
	else:
		return False
		
pythonista = is_pythonista()

if pythonista:
	import console
	import editor

def to_abs_path(*value):
	import os, sys
	if 'Pythonista' in sys.executable:
		abs_path = os.path.join(os.path.expanduser('~'),'Documents')
	else:
		abs_path = os.getcwd()
		
	for _value in value:
		abs_path = os.path.join(abs_path,_value)
	return abs_path

def downloader(url, file_path, progress=True, style=1):
	_file_path = os.path.basename(file_path)
	with open(file_path, "wb") as f:
		print("Downloading %s" % _file_path)
		response = requests.get(url, stream=True)
		total_length = response.headers.get('content-length')
		
		f.write(response.content)
		
url = 'https://raw.githubusercontent.com/nekotaroneko/Transfer/master/Transfer.py'
script_path = to_abs_path('site-packages-2/Transfer.py') if pythonista else os.path.join(os.getcwd(), 'Transfer.py')
startup_path = to_abs_path('site-packages-2/pythonista_startup.py')

if os.path.exists(script_path):
	os.remove(script_path)
	
downloader(url, script_path)

assert os.path.exists(script_path), 'Error'
print('{} was created'.format(script_path))

if pythonista:
	editor.open_file(script_path, True)
	with open(startup_path, "r+") as file:
		if not 'Transfer' in file.read() and console.alert('Transfer Installer', 'Start UP?', "No","Yes",hide_cancel_button=True) == 2:
			file.write('''import Transfer\nTransfer.start_up()''')
			console.alert('Transfer Installer', 'Added two lines to site-packages-2/pythonista_startup.py', 'OK', hide_cancel_button=True)
			