# coding: utf-8

# https://gist.github.com/jsbain/fcb3f42932dde9b0ff6c122893d1b230

import requests
import appex,console,time,os

unquote=requests.utils.unquote
urlparse=requests.utils.urlparse
url=appex.get_url()
p=urlparse(url)
urlfilename=unquote(unquote(urlparse(appex.get_url()).path.split('/')[-1]))
console.hud_alert('downloading '+urlfilename)
console.show_activity()
if p.netloc.startswith('gist.github.com'):
	gist_id=urlfilename
	data=requests.get('https://api.github.com/gists/{}'.format(gist_id)).json()
	if data:
		gistpath=os.path.expanduser('~/Documents/gists/')
		destpath=os.path.join(gistpath,gist_id)
		for pth in [gistpath, destpath]:
			if not os.path.exists(pth):
				os.mkdir(pth)
		for f in data['files'].values():
			filename=f['filename']
			console.hud_alert('writing '+filename)
			url=f['raw_url']
			#rather than deal with possibly truncated files, or unicode, just download raw url as binary
			with open(os.path.join(destpath,filename),'wb') as file:
				file.write(requests.get(url).content)
	else:
		console.hud_alert('could not download')
else:
	destpath=urlfilename
	with open(destpath,'wb') as file:
		file.write(requests.get(url).content)


console.hud_alert(urlfilename +' complete')
console.hide_activity()
appex.finish()
