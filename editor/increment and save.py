# http://omz-forums.appspot.com/pythonista/post/5903756180848640
# https://gist.github.com/weakmassive/2400bcca3ae2c0a6a43c

# This Pythonista script increments and saves the current file.
# I wrote it so I could quickly save different versions of scripts.
# It is meant to be added to the editor's action menu.

import editor, os, re
text = editor.get_text()
if not text:
	sys.exit('No text in the Editor.')
	
filename = os.path.split(editor.get_path())[1][:-3]

#finds number at end
num = re.split('[^\d]', filename)[-1]

#check if number string is empty
#if file ends with a number, increment it
l = len(num)

if l >=1:
	num2 = int(num) + 1
	filename = filename[:-l] + str(num2) + ".py"
else:
	filename = filename + str(1) + ".py"
	
#write new file
editor.make_new_file(filename, text)

