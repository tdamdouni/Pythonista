#!/usr/bin/python

import sys
import editor
import os
import errno
import base64

path = sys.argv[1] #The path sent through with the x-callback-url.
text = base64.b64decode(sys.argv[2]) # The text from the file

#Create directory structure if missing
try:
	os.makedirs(os.path.join(os.path.expanduser('~/Documents'), path))
except OSError, e:
	#only pass if directory exists
	if e.errno != errno.EEXIST:
		raise e
	pass

fullPath = os.path.join(os.path.expanduser('~/Documents'), path)
with open(fullPath, 'w') as f: # To clear the file.
	f.write(text) # Write the new code to the file.		

#To refresh contents in Pythonista
editor.open_file(path)
console.hud_alert(path +' Updated')