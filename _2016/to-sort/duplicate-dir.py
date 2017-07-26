# https://forum.omz-software.com/topic/3586/duplicate-a-directory-or-multiple-files/5

import editor, clipboard, re, console, os

'''Utilities to be added to the editor
'''
def copyDirPathToClipboard():
	'''Copy current file directory to the clipboard
	'''
	# get current location
	file = editor.get_path()
	dir = os.path.dirname(file)
	
	# inform user and get confirmation
	msg = re.match('.*Pythonista3/Documents/(.+)',dir).group(1)
	ans = console.alert('Copy','Copy this directory?\n'+msg+'\nNB: select a file to get its directory!','yes')
	
	# if yes, copy to clipboard
	if ans == 1 :
		clipboard.set(dir)
		console.hud_alert('Done!','success',0.5)
		
copyDirPathToClipboard()

# 

import editor, clipboard, console, re, shutil, os

'''Utility to be added to the editor
'''
def pasteDir():
	'''Copy the directory in clipboard to the same directory as the current file
	'''
	# get current directory location
	file = editor.get_path()
	dir = os.path.dirname(file)
	
	# get source directory from clipboard
	src = clipboard.get()
	
	# get name of directory
	name = src.split('/')
	name = name[-1]
	
	# build destination name
	dst = dir + '/' + name
	
	# short version of destination
	msg = re.match('.*Pythonista3/Documents/(.+)',dst).group(1)
	
	# if already exists then cancel
	if os.path.exists(dst):
		console.alert('Paste Error','Directory:\n'+ msg + '\nalready exists! Paste not possible.')
		
	# inform user and get confirmation
	ans = console.alert('Paste','Create this new directory?\n'+msg,'yes')
	
	# if yes, paste
	if ans == 1:
		shutil.copytree(src,dst)
		console.hud_alert('Done!','success',0.5)
		
		
pasteDir()

