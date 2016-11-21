# coding: utf-8

# https://gist.github.com/bmw1821/d9883042b95a818e6429

def main()
	import requests
	
	PydiaKit_content = requests.request('GET', 'https://dl.dropboxusercontent.com/s/ja5fqva5jkgz6l0/PydiaKit.py?dl=0').content
	PydiaPackage_content = requests.request('GET', 'https://dl.dropboxusercontent.com/s/l0zaw0p865hsqrt/Pydia_Package.py?dl=0').content
	PydiaSources_content = requests.request('GET', 'https://dl.dropboxusercontent.com/s/6umbih2wep3puzv/Pydia_Sources.py?dl=0').content
	Pydia_UI_Main_content = requests.request('GET', 'https://dl.dropboxusercontent.com/s/uvgotwa7717nm9v/Pydia_UI.py?dl=0').content
	
	site-packages = os.path.expanduser('~/Documents/site-packages/')
	
	open(site-packages + 'PydiaKit.py', 'w').write(PydiaKit_content)
	
	for folder in ['Package Support', 'Pydia Sources', 'Pydia Supporting Files', 'Pydia Supporting Files/Pydia UI', 'Pydia User Info']:
		dir = site-packages + 'Pydia/' + folder
		if not os.path.exists(dir):
			os.makedirs(dir)
			
	open(site-packages + 'Pydia/Pydia Supporting Files/PydiaPackage.py', 'w').write(PydiaPackage_content)
	open(site-packages + 'Pydia/Pydia Supporting Files/PydiaSources.py', 'w').write(PydiaSources_content)
	open(site-packages + 'Pydia/Pydia Supporting Files/Pydia UI/Pydia_UI.py', 'w').write(Pydia_UI_Main_content)
	
	if not os.path.exists(site-packages + 'Pydia/Pydia User Info/Sources.py'):
		open(site-packages + 'Pydia/Pydia User Info/Sources.py', 'w').write('{}')
	if not os.path.exists(site-packages + 'Pydia/Pydia User Info/Installed Packages.py'):
		open(site-packages + 'Pydia/Pydia User Info/Installed Packages.py', 'w').write('{"com.Pydia.Source": "https://bit.ly/Pydia"}')
		
if __name__ == '__main__':
	main()

