# coding: utf-8

# https://gist.github.com/ScottSmith95/2f9b249f9e6e0e9fc6ef

''' This script allows you to copy a .py script to the iOS clipboard and then use Open In...
to have that script saved in Pythonista.

This requires both the Workflow and Pythonista apps
and either of the following Workflows:
Save in Pythonista (from Workflow Action Extension) https://workflow.is/workflows/80c7bee7a6c446dc872964600ddd57fd
Open in Pythonista (from Document Picker) https://workflow.is/workflows/e68fdf26479d473b92443a9a69fe176c

Adapted from: https://github.com/mncfre/Save-Script '''

import clipboard
import console
import os
import sys

def save(filename, text, ext):
	root, _ = os.path.splitext(filename)
	extension = ext
	filename = root + extension
	filenum = 1
	while os.path.isfile(filename):
		filename = '{} {}{}'.format(root, filenum, extension)
		filenum += 1
	with open(filename,'w') as f:
		f.write(text)
	#clipboard.set(filename)
	return filename

def main():
	#print sys.argv[:]
	
	filename = sys.argv[1]
	
	resp = console.alert(
		'Choose File Extension',
		'',
		'Detect Extension'+' (.'+sys.argv[2]+')',
		'.py',
		'Custom',
		hide_cancel_button=False
	)
	if resp==1:
		ext = '.'+sys.argv[2]
	elif resp==2:
		ext = '.py'
	elif resp==3:
		ext = console.input_alert('File extension', 'Type a file extension.', '.')
	
	if len(sys.argv) > 3:
		text = sys.argv[3]
	elif clipboard.get():
		text = clipboard.get()
		#console.alert('Used clipboard')
	assert text, 'No text captured!'
	
	console.clear()
	print('Wait a Moment Please!')
	console.clear()
	filename = save(filename, text, ext)
	print('Done!\nFile Saved as:\n' + filename)
	
if __name__ == '__main__':
	main()
