# coding: utf-8

# https://forum.omz-software.com/topic/2711/open-page-source-in-pythonista

import appex
import urllib2
from objc_util import *
#Helper functions
def openUrl(url):
	'''Allows webbrowser.open()-esque functionality from the app extension'''
	app=UIApplication.sharedApplication()
	app._openURL_(nsurl(url))
def getDocPath():
	'''Gets the path to ~/Documents'''
	split=__file__.split('/')
	path=split[:split.index('Documents')+1]
	return '/'.join(path)+'/'
#Get the url
url=appex.get_url()

# ...
#Read page contents
import requests
r = requests.get(url)
source = r.text
ct = r.headers['Content-Type']
# A fancier version could use the mimetypes module to guess the proper file extension...
extension = '.html' if ct.startswith('text/html') else '.txt'
# ...

#Read page contents
#f=urllib2.urlopen(url)
#source=f.read()
#f.close()
#Detect the type of page we're viewing
#test=source.lower().strip()
#if '<html>' in test or test.startswith('<!doctype html>'): #Page is HTML
	#extension='.html'
#else: #fallback to .txt
	#extension='.txt'
	
#Where to save the source
filename='source'+extension
filepath=getDocPath()+filename
#Save the source
with open(filepath,'w') as f:
	f.write(source)
#Close appex window
appex.finish()
#Open in pythonista
openUrl('pythonista://'+filename)

