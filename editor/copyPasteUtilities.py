# https://gist.github.com/anonymous/23407f680c9744ad2beb6d1fafcca9a4

# https://forum.omz-software.com/topic/3586/duplicate-a-directory-or-multiple-files/11

'''This script installs two utilities in the editor:
        copy directory
        paste directory
        Author: Jmv38 - 2016 - Pythonista3
'''
import editor, clipboard, console, re, shutil, os

from sys import argv

# this code is from JonB - Thank you!
# source: https://github.com/jsbain/objc_hacks/blob/master/add_action.py

from objc_util import *
NSUserDefaults = ObjCClass('NSUserDefaults')

def add_action(scriptName,iconName='python',iconColor='',title='',arguments=''):
	'''adds an editor action.  scriptName should start with /
	(e.g /stash/stash.py)
	iconName should be an icon without leading prefix, or trailing size.  i.e alert instead of iob:alert_256
	iconColor should be a web style hex string, eg aa00ff
	title is the alternative title
	Call save_defaults() to store defaults
	')'''
	defaults=NSUserDefaults.standardUserDefaults()
	kwargs=locals()
	entry={ key:kwargs[key]
	for key in
	('scriptName','iconName','iconColor','title','arguments')
	if key in kwargs and kwargs[key] }
	editoractions=get_actions()
	editoractions.append(ns(entry))
	defaults.setObject_forKey_(editoractions,'EditorActionInfos')
	
def remove_action(scriptName):
	''' remove all instances of a given scriptname.
	Call save_defaults() to store for next session
	'''
	defaults=NSUserDefaults.standardUserDefaults()
	editoractions=get_actions()
	[editoractions.remove(x) for x in reversed(editoractions) if str(x['scriptName'])==scriptName]
	defaults.setObject_forKey_(editoractions,'EditorActionInfos')
	
def remove_action_at_index(index):
	''' remove action at index.  Call save_defaults() to save result.
	'''
	defaults=NSUserDefaults.standardUserDefaults()
	editoractions = get_actions()
	del editoractions[index]
	defaults.setObject_forKey_(editoractions,'EditorActionInfos')
	
def get_defaults_dict():
	'''return NSdictionary of defaults'''
	defaults=NSUserDefaults.standardUserDefaults()
	return defaults.dictionaryRepresentation()
	
def get_actions():
	'''return action list'''
	defaults=NSUserDefaults.standardUserDefaults()
	return list(defaults.arrayForKey_('EditorActionInfos'))
	
def save_defaults():
	'''save current set of defaults'''
	defaults=NSUserDefaults.standardUserDefaults()
	NSUserDefaults.setStandardUserDefaults_(defaults)
	
# end of JonB code

def install_actions():
	''' Installs shortcuts in the wrench menu
	'''
	# get current location
	file = editor.get_path()
	file = re.match('.+Pythonista3/Documents(/.+)',file).group(1)
	
	# remove previous shortcuts
	remove_action(file)
	
	# and install new ones
	count = 0
	
	cmd = 'copy_dir'
	add_action(arguments = cmd,
	iconName = "ios7-copy",
	iconColor = '020202',
	scriptName = file,
	title = cmd )
	count+=1
	
	cmd = 'paste_dir'
	add_action(arguments = cmd,
	iconName = "Primaries_Paste",
	iconColor = '020202',
	scriptName = file,
	title = cmd )
	count+=1
	
	cmd = 'copy_file'
	add_action(arguments = cmd,
	iconName = "ios7-copy",
	scriptName = file,
	title = cmd )
	count+=1
	
	cmd = 'paste_file'
	add_action(arguments = cmd,
	iconName = "Primaries_Paste",
	scriptName = file,
	title = cmd )
	count+=1
	
	save_defaults()
	
	if count > 0:
		console.hud_alert(str(count)+' shortcuts installed','success',1)
	else:
		console.hud_alert('Shortcuts already installed','error',1)
		
def copyDir():
	'''Copy current file directory to the clipboard
	'''
	# get current location
	file = editor.get_path()
	dir = os.path.dirname(file)
	
	# inform user and get confirmation
	msg = re.match('.*Pythonista3/Documents/(.+)',dir).group(1)
	ans = console.alert('Copy',
	'\nNB: YOU MUST SELECT A FILE IN THE DIRECTORY TO COPY!'
	+ '\n\nIs this the directory you want to copy?\n\n' + msg
	,'yes')
	
	# if yes, copy to clipboard
	if ans == 1 :
		clipboard.set(dir)
		console.hud_alert('Done!','success',0.5)
		
		
def pasteDir():
	'''Copy the directory in clipboard to the same directory as the current file
	'''
	# get current directory location
	file = editor.get_path()
	dir = os.path.dirname(file)
	
	# get source directory from clipboard
	src = clipboard.get()
	
	# is it a valid source?
	if not os.path.exists(src):
		console.alert('Paste Error',
		'Directory described in clipboard does not exist! Paste not possible.'
		+ '\nClipboard content:\n\n' + src)
		return
	msg = re.match('.+(Pythonista3/Documents/)(.+)',src)
	if (msg == None) or (msg.group(2) == None):
		msg = 'clipboard content is not a valid pythonista3 sub-directory:\n'+src+'\npaste not possible.'
		console.alert('Paste Error', msg)
		return
		
	# get name of directory
	name = msg.group(2)
	name = name.split('/')[-1]
	
	# build destination name
	dst = dir + '/' + name
	# and a short version
	msg = re.match('.+(Pythonista3/Documents/)(.+)',dst).group(2)
	
	# if already exists then cancel
	if os.path.exists(dst):
		console.alert('Paste Error','Directory:\n'+ msg + '\nalready exists! Paste not possible.')
		return
		
	# inform user and get confirmation
	ans = console.alert('Paste',
	'\nNB: YOU MUST SELECT A FILE IN THE DIRECTORY WHERE TO PASTE!'
	+ '\n\nIs this the directory you want to create?\n\n' + msg
	,'yes')
	
	# if yes, paste
	if ans == 1:
		shutil.copytree(src,dst)
		console.hud_alert('Done!','success',0.5)
		
def copyFile():
	'''Copy current file to the clipboard
	'''
	# get current file
	file = editor.get_path()
	
	# get short version
	filepath,filename = os.path.split(file)
	
	# inform user and get confirmation
	ans = console.alert('Copy',
	'\n\nIs this the file you want to copy?\n\n' + filename
	,'yes')
	
	# if yes, paste
	if ans == 1:
		# copy to clipboard
		clipboard.set(file)
		console.hud_alert('Done!','success',0.5)
		
def pasteFile():
	'''Copy the filename in clipboard to the same directory as the current file
	'''
	# get current directory location
	file = editor.get_path()
	dir = os.path.dirname(file)
	
	# get source file from clipboard
	src = clipboard.get()
	
	# is it a valid source?
	if not os.path.isfile(src):
		console.alert('Paste Error',
		'File described in clipboard does not exist! Paste not possible.'
		+ '\nClipboard content:\n\n' + src)
		return
		
	# get name of file
	filepath,filename = os.path.split(src)
	
	# build destination name
	dst = dir + '/' + filename
	# and a short version
	msg = re.match('.+(Pythonista3/Documents/)(.+)',dst).group(2)
	
	# if already exists then cancel
	if os.path.isfile(dst):
		console.alert('Paste Error','File:\n\n'+ msg + '\n\nalready exists! Paste not possible.')
		return
		
	# inform user and get confirmation
	ans = console.alert('Paste',
	'\n\nIs this the file you want to create?\n\n' + msg
	,'yes')
	
	# if yes, paste
	if ans == 1:
		shutil.copy2(src,dst)
		console.hud_alert('Done!','success',0.5)
		
		
# get script argument
cmd = argv[-1]
if cmd == 'paste_dir':
	pasteDir()
elif cmd == 'copy_dir':
	copyDir()
elif cmd == 'copy_file':
	copyFile()
elif cmd == 'paste_file':
	pasteFile()
else:
	install_actions()

