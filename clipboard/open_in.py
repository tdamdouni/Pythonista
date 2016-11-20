# coding: utf-8

# http://omz-forums.appspot.com/pythonista/post/5862307733176320

# https://gist.github.com/pysmath/59c9b38e127827e2d6ed

''' This script allows you to copy a .py script to the iOS clipboard and then use Open In...
to have that script saved in Pythonista.  This requires both the Workflow and Pythonista apps
and the workflow at https://workflow.is/workflows/8cdee57f79664205a6a565c9cbdb3d48 '''

import clipboard
import console
import os
import sys
import editor

def save(filename, text, ext):
	root, _ = os.path.splitext(filename)
	extension = ext
	filename = root.replace('\n','') + extension
	filenum = 1
	while os.path.isfile(filename):
		filename = '{} {}{}'.format(root, filenum, extension)
		filenum += 1
	with open(filename,'w') as f:
		f.write(text)
	return filename
	
def main():
	resp = console.alert('Alert!', 'Choose File Extension', '.py', '.pyui', 'other', hide_cancel_button=False)
	if resp==1:
		ext = '.py'
	elif resp==2:
		ext = '.pyui'
	elif resp==3:
		ext = console.input_alert('Specify file extension')
	text = clipboard.get()
	assert text, 'No text on the clipboard!'
	filename = sys.argv[1]
	console.clear()
	filename = save(filename, text, ext)
	editor.open_file(filename)
	
if __name__ == '__main__':
	main()

