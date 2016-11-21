# coding: utf-8

# https://gist.github.com/balachandrana/d7dcaf3aadef5dbe633768d477898eb9

# https://forum.omz-software.com/topic/2905/helper-script-for-embedding-pyui-files-in-single-file-scripts/2

# Sharing pyui file is simplified by the following omz's script.
# https://forum.omz-software.com/topic/2905/helper-script-for-embedding-pyui-files-in-single-file-scripts
# This may be good enough if users just want to run the script.
# But if they want to see or edit the .pyui file, it would be helpful
# to generate the .pyui file. This script does this geneartion.
# This script extracts the encoded string, decode it and
# generate the .pyui file. Like the embedpyui script,
# this needs to be added to editor actions (wrench) menu.
#

import bz2
import re
from base64 import b64decode
import editor
import codecs

def main():
	# get text between single triple quotes
	# skip the first two characters, backslash and newline
	data = re.split("""'''""", editor.get_text())[1][2:]
	#print(data[:10])
	
	# decode as in omz's script and write it in .pyui file
	pyui = bz2.decompress(b64decode(data))
	filename = editor.get_path()[:-3] + '.pyui'
	#print (filename)
	with codecs.open(filename, "w", 'utf-8') as fp:
		fp.write(pyui.decode('utf-8'))
		
if __name__ == '__main__':
	main()

