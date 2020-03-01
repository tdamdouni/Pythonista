# coding: utf-8

# https://forum.omz-software.com/topic/2775/cloud-import/19

import os

DOCS_DIR = os.path.expanduser('~/Documents/')
SITE_DIR = os.path.join(DOCS_DIR, 'site-packages/')

#==============================

{
    "pythonista": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "pythonista.app": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "pythonista.editor": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "pythonista.console": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "Gestures": "https://github.com/mikaelho/pythonista-gestures"
}

#==============================

import json

with open("modules.json", "r") as f:
	modules = json.load(f)
	
#==============================

import requests

modules = requests.get("https://example.com/modules.json").json

#==============================


import cloud

cloud.Import('pythonista.editor')
cloud.Import('Gestures')

pythonista.editor.WebTab().present()
g = Gestures.Gestures()

# coding: utf-8

''' cloud.py '''

import bs4, urllib2, plistlib, shutil, zipfile, os, importlib, inspect

def Import(sTarget):
	for code in bs4.BeautifulSoup(urllib2.urlopen('http://forum.omz-software.com/topic/2775/cloud-import').read()).find_all('code'):
		s = code.getText()
		if s[:5] == '<?xml': urlZ = plistlib.readPlistFromString(s)[sTarget] + '/archive/master.zip'
	sZ = os.path.expanduser('~/Documents/'+  urlZ.split('/')[-1])
	shutil.copyfileobj(urllib2.urlopen(urlZ), open(sZ, 'wb'), length=512*1024)
	with open(sZ, 'rb') as f:
		for member in zipfile.ZipFile(f).namelist():
			l = member.split('/')
			if len(l) <= 2: # module
				if l[-1][-3:] == '.py':
					zipfile.ZipFile(f).extract(member, os.path.expanduser('~/Documents/'))
					shutil.move(os.path.expanduser('~/Documents/'+ member), os.path.expanduser('~/Documents/site-packages/' + l[-1]))
			else: # package
				if l[1] == sTarget.split('.')[0] and l[-1] != '':
					zipfile.ZipFile(f).extract(member, os.path.expanduser('~/Documents/'))
					if not os.path.exists(os.path.expanduser('~/Documents/site-packages/' + l[-2])):
						os.mkdir(os.path.expanduser('~/Documents/site-packages/' + l[-2]))
					shutil.move(os.path.expanduser('~/Documents/'+ member), os.path.expanduser('~/Documents/site-packages/' + l[-2] + '/' + l[-1]))
	shutil.rmtree(os.path.expanduser('~/Documents/' + l[0]))
	os.remove(sZ)
	if len(sTarget.split('.')) == 1: # module
		locals()[sTarget.split('.')[0]] = importlib.import_module(sTarget.split('.')[0])
	else: # package
		locals()[sTarget.split('.')[0]] = importlib.import_module(sTarget.split('.')[0])
		locals()[sTarget.split('.')[1]] = importlib.import_module(sTarget)
	reload(locals()[sTarget.split('.')[0]])
	inspect.currentframe().f_back.f_globals[sTarget.split('.')[0]] = locals()[sTarget.split('.')[0]]

