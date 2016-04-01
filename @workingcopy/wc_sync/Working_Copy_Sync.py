import ui
import editor
import os
import console
import webbrowser as wb
import urllib
import base64
import keychain

#This should not have leading or trailing /
INSTALL_PATH = 'wc_sync'

#Key set in checkKey funtion
key = None

def close_view(sender):
	sender.superview.close()

def info():
	documentsDir = os.path.expanduser('~/Documents')
	info = editor.get_path()
	fullPath = info[len(documentsDir)+1:] # get the relative path and remove the leading /
	path = fullPath.split('/',1)[1]
	repo = fullPath.split('/',1)[0]
	return repo,path
	
def sendB64(repo,path,text):
	url = 'working-copy://x-callback-url/write/?'
	b64 = base64.b64encode(text)
	f = {'repo':repo,'path':path,'key':key,'base64':b64,'x-success':'pythonista://'+repo+'/'+path+'?'}
	url += urllib.urlencode(f).replace('+','%20')
	wb.open(url)

def sendText(repo,path,text):
	url = 'working-copy://x-callback-url/write/?'
	f = {'repo':repo,'path':path,'key':key,'text':text,'x-success':'pythonista://'+repo+'/'+path+'?'} # add repo and path to pythonista call back in order to not receive an error
	url += urllib.urlencode(f).replace('+','%20')
	wb.open(url)
	
def open_wc(sender): # Opens working copy
	repo, path = info()
	url = 'working-copy://open?'
	f = {'repo':repo}
	url += urllib.urlencode(f).replace('+','%20')
	wb.open(url)
	sender.superview.close()

@ui.in_background
def copyFromWCPt1(sender):
	''' Copies the text from the working copy version 
			of the file and uses it to overwrite the contents 
			of the corresponding file in pythonista.
	'''
	repo,path = info()
	url = 'working-copy://x-callback-url/read/?'
	success = 'pythonista://'+INSTALL_PATH+'/rxFile.py?action=run&argv=' + os.path.join(repo,path) +'&argv='
	f = {'repo':repo,'path':path,'key':key, 'base64':'1'}
	url += urllib.urlencode(f).replace('+','%20')
	url += '&x-success=' + urllib.quote_plus(success)
	wb.open(url)
	sender.superview.close()

def sendToWCPt1(sender):
	''' Sends the contents of the file in pythonista 
			to overwrite the working copy version.
	'''
	repo,path = info()
	sendText(repo,path,editor.get_text())
	sender.superview.close()

def sendPYUIToWCPt1(sender):
	''' Send pyui to working copy 
	'''
	repo,path = info()
	path += 'ui'
	fullPath = os.path.join(os.path.expanduser('~/Documents'), os.path.join(repo,path))
	try:
		with open(fullPath) as file:
			sendB64(repo,path,file.read())
	except IOError:
		console.alert('No PYUI file associated. Now say you\'re sorry.' ,button1='I\'m sorry.', hide_cancel_button=True)
	sender.superview.close()
		
def getZipPt1(sender):
	''' copy a repo to the local filesystem 
	'''
	repo = console.input_alert('Repo name')
	if repo: 
		url = 'working-copy://x-callback-url/zip/?'
		f = {'repo':repo, 'key':key}
		success ='pythonista://'+INSTALL_PATH+'/rxZip.py?action=run&argv='+repo+'&argv='
		url += urllib.urlencode(f).replace('+','%20')
		url += '&x-success=' + urllib.quote_plus(success)
		wb.open(url)
	else:
		console.alert('Invalid repo name')
	sender.superview.close()

def checkKey():
	global key
	key = keychain.get_password('wcSync','xcallback')
	if key == None:
		pwd = console.password_alert('Working Copy Key')
		keychain.set_password('wcSync','xcallback',pwd)
	
def main():
	checkKey()
	view = ui.load_view('Working_Copy_Sync')
	width, height = ui.get_screen_size()
	try:
		if width >= 768:
			view.present('sheet', hide_title_bar=True)
		else:
			view.present(hide_title_bar=True)
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()