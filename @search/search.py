#coding: utf-8

# https://gist.github.com/pfcbenjamin/c2852b22663aaa66011c

'''
A little script to search Google or GitHub right from inside Pythonista. 
I added the script to the action menu so I can do a quick search without leaving Pythonista. 
I find this especially helpful if I'm researching some error my script is throwing.
'''

import webbrowser
import console
import urllib
import re

def SiteSearch(term,service):
	if service == 1:
		tencode = urllib.quote(term)
		url = 'https://www.google.com/search?q=' + tencode
		return webbrowser.open(url)
	elif service == 2:
		tencode = re.sub('\s','+',term)
		url = 'https://gist.github.com/search?l=python&q=' + tencode
		return webbrowser.open(url)
	elif service == 3:
		tencode = re.sub('\s','+',term)
		url = 'https://github.com/search?l=Python&q=' + tencode
		return webbrowser.open(url)
	else:
		console.hud_alert('Please select a service to search.','error')

term = console.input_alert('Search Term')
service = console.alert('where would you like to search?','','Google','GitHub (Gist)','GitHub (Repo)',)

#url = 'https://www.google.com/search?q=' + tencode

SiteSearch(term,service)