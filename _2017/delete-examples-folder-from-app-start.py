# https://forum.omz-software.com/topic/4227/how-to-get-rid-of-examples-folder-and-contents

import shutil,os
try:
	shutil.rmtree(os.path.expanduser('~/Documents')+'/Examples')
except:
	pass
