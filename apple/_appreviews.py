
# Pythonista script
# Script name: getreviews.py
# Author: Olivier HO-A-CHUCK
# License (OHO Ware): free to use modify, alter, re-use for commercial use or not! :)
# Date: Nov. 15th 2012 
# Usage through URL Scheme: pythonista://_appreviews?action=run&args=<appID>
# exemple: pythonista://_appreviews?action=run&args=308816822
# hint: you can create links like that on note application on iPhone or iPad (as links with url schemes are clickable)

import json
import urllib2
import re
import console
import clipboard
import sys

if len(sys.argv) == 1:
  appID = '528579881' #Pythonista
else:
	appID = sys.argv[1]

url = 'http://itunes.apple.com/fr/rss/customerreviews/id=' + appID + '/sortby=mostrecent/json'

console.clear()
response = urllib2.urlopen(url)
content = response.read()
data = json.loads(content.decode("utf8"))
text	 = ''
print("Application ID: " + appID)
text += "Application ID: " + appID + "\n"
lastUpdate = data['feed']['updated']['label']
print("last comments update: " + lastUpdate)
text += "last comments update: " + lastUpdate + "\n\n"
lastPage = data['feed']['link'][3]['attributes']['href']
#print(lastPage)
nbPages = int(re.findall(r".*page=(\d*)/.*", lastPage)[0])
print("Theoritical number of pages: " + str(nbPages))
maxPages = nbPages
maxPages = maxPages if nbPages < 10 else 10
print("Using " + str(maxPages) + " pages ...\n\n");

i = 0
page = 1
while page < maxPages+1:
#while page < int(nbPages)+1:
	urlPos = re.sub("customerreviews","customerreviews/page="+str(page),url)
	response = urllib2.urlopen(urlPos)
	content = response.read()
	data = json.loads(content.decode("utf8"))
	if len(data['feed']['entry']) == 11:	# if script does not work anymore, check if this is still true!
		page += 1
		continue
	for entryIndex in data['feed']['entry']:
		if i == 0:
			i = 1
			continue
		#print(str(i) + ": " + entryIndex['title']['label'])
		version = entryIndex['im:version']['label']
		rating = entryIndex['im:rating']['label']
		title = entryIndex['title']['label']
		author = entryIndex['author']['name']['label']
		content = entryIndex['content']['label']
		print(str(page) +"."+ str(i) + ": " + "("+ version +") "+ rating + "* [" + author + "] " + title)
		text += str(page) +"."+ str(i) + ": " + "("+ version +") "+ rating + "* [" + author + "] " + title + "\n"
		print(content+"\n--")
		text += content+"\n--\n"
		i += 1
	page += 1
	i = 0
	
clipboard.set(text)