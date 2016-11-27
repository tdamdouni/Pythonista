# coding: utf-8

# https://gist.github.com/Mr-Coxall/4ae9e8a9e49e0121e93284b318b70bea

# Created By: jsbain -> https://gist.github.com/jsbain
# Created For: Pythonista
# Created On: Aug-2016

# Altered on: Aug 2016
# Altered by: Mr. Coxall
# What Changed: added comments, changed name of file, changed the output the user sees

# Best used through the shar sheet in iOS Safari
# this code is used to download a GIST that you are looking at in Safari
# right into Pythonista

import requests
import appex,console,time,os

unquote=requests.utils.unquote
urlparse=requests.utils.urlparse
url=appex.get_url()
p=urlparse(url)
urlfilename=unquote(unquote(urlparse(appex.get_url()).path.split('/')[-1]))
console.hud_alert('Downloading the Gist, please wait.')
console.show_activity()
if p.netloc.startswith('gist.github.com'):
	gist_id=urlfilename
	data=requests.get('https://api.github.com/gists/{}'.format(gist_id)).json()
	if data:
		gistpath=os.path.expanduser('~/Documents/Downloaded Gists/')
		destpath=os.path.join(gistpath,gist_id)
		for pth in [gistpath, destpath]:
			if not os.path.exists(pth):
				os.mkdir(pth)
		for f in data['files'].values():
			filename=f['filename']
			console.hud_alert('writing '+filename)
			content=f['content']
			with open(os.path.join(destpath,filename),'w') as file:
				file.write(content)
	else:
		console.hud_alert('could not download')
else:
	destpath=urlfilename
	with open(destpath,'wb') as file:
		file.write(requests.get(url).content)


console.hud_alert('Download complete')
console.hide_activity()
appex.finish()
