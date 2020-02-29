from __future__ import print_function
# https://gist.github.com/Mr-Coxall/7fbf6dc0ec3d83525f1944812ccce46f

# https://forum.omz-software.com/topic/3435/gist-file-retrieval/9

# Created by: jsbain
# Created on: Aug 2014
# URL : https://github.com/jsbain/GitHubGet/blob/master/GitHubGet.py

# download an entire github repo.
# either copy the url to clipboard, and run script, or run following bookmarklet.
# will unzip to repo-branch (so be careful if downloading same branch name from multiple users)
#
##   javascript:(function()%7Bif(document.location.href.indexOf('http')===0)document.location.href='pythonista://GitHubGet?action=run&argv='+document.location.href;%7D)();

# Altered by: Mr. Coxall
# Altered on: Aug 2016
# Combined with other code, so that it will only work from sharesheet
#     and gives the user different and better feedback
# Also places the files in Downloaded from Github directory
# This works not only with Github repos but also Gists.

import requests
import appex, console, time, os
import urllib, zipfile, sys, functools, re, os, tempfile
#import urllib,zipfile,sys, clipboard, functools, re, os, tempfile

def extract_git_id(git):
	#print git
	m = re.match((r'^http(s?)://([\w-]*\.)?github\.com/(?P<user>[\w-]+)/(?P<repo>[\w-]*)'
	'((/tree|/blob)/(?P<branch>[\w-]*))?'), git)
#    print m.groupdict()
	return m
	
def git_download_from_args(args):
	if len(args) == 2:
		url = args[1]
	else:
		url = clipboard.get()
		#print(url)
	git_download(url)
	
def git_download_from_sharesheet():
	if appex.is_running_extension():
		#unquote=requests.utils.unquote
		#urlparse=requests.utils.urlparse
		url = appex.get_url()
		#print(url)
		git_download(url)
	else:  # Error handling...
		print('''=====
		* In Safari browser, navigate to a GitHub repo or Gist of interest.
		* Tap 'Open in...' icon in top right of Safai window.
		* Tap 'Run Pythonista Script'.
		* Pick this script and tap the run button.
		* When you return to Pythonista the files should be in '~/Documents/Downloaded from Github/'.''')
		
		
def dlProgress(filename, count, blockSize, totalSize):
	if count*blockSize > totalSize:
		percent=100
	else:
		percent = max(min(int(count*blockSize*100/totalSize),100),0)
	sys.stdout.write("\r" + filename + "...%d%%" % percent)
	sys.stdout.flush()
	
def git_download(url):
	base = 'https://codeload.github.com'
	archive = 'zip'
	m = extract_git_id(url)
	if m:
		g = m.groupdict()
		if not g['branch']:
			g['branch'] = 'master'
			
		u = '/'.join((base,g['user'],g['repo'],archive, g['branch']))
		#print u
		#console.hud_alert('Downloading Github repo ...' + u)
		console.hud_alert('Starting, please wait.')
		console.show_activity()
		try:
			with tempfile.NamedTemporaryFile(mode='w+b',suffix='.zip') as f:
				console.hud_alert('Downloading the zip.')
				urllib.urlretrieve(u,f.name,reporthook=functools.partial(dlProgress,u))
				
				z = zipfile.ZipFile(f)
				githubpath = os.path.expanduser('~/Documents/Downloaded from Github/')
				if not os.path.exists(githubpath):
					os.mkdir(githubpath)
				z.extractall(path = githubpath)
				console.hud_alert('Extracting zip.')
				print(z.namelist())
		except:
			print('git url did not return zip file')
		console.hud_alert('Files saved in "Downloaded from Github" directory.')
		console.hud_alert('All done.')
	else:
		print('could not determine repo url from clipboard or argv')
		
if __name__=='__main__':
	#git_download_from_args(sys.argv)
	git_download_from_sharesheet()

