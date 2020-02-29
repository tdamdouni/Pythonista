# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/f2a3a9e225d4c0ffb62f

# Download File Extension

from __future__ import print_function
import urllib2, appex, time, zipfile, os
a=time.time()
if appex.is_running_extension():
	url = appex.get_url()
	print(url)
	e=0
else:
	import clipboard, editor
	url = clipboard.get()
	e=1

response = urllib2.urlopen(url)
file = response.read()

name = url.split('/')[-1]
home = '/private/var/mobile/Containers/Shared/AppGroup/0BE72E31-5474-44B2-9731-3686B8BF7EDC/Documents/'
output = open(home+name, 'w')
output.write(file)
output.close()

print('Downloaded '+name+' to /Documents/'+name+' in '+str(time.time()-a)+' seconds')

if zipfile.is_zipfile(home+name):
	print('Extracting zip...')
	zipfile.ZipFile(home+name).extractall(home)
	os.remove(home+name)
if e:
	editor.reload_files()