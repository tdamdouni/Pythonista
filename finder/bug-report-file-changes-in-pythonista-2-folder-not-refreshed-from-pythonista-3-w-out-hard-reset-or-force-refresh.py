# coding: utf-8

# https://forum.omz-software.com/topic/3087/bug-report-file-changes-in-pythonista-2-folder-not-refreshed-from-pythonista-3-w-out-hard-reset-or-force-refresh

import FileB
from FileB import *

class FileAClass(object):
	def __init__(self):
		self.remote = FileB.FileBClass()
		
if __name__ == "__main__":
	local = FileAClass()
	
	local.remote.functionB()
	standaloneFunction()
	
# --------------------

# coding: utf-8

import time


class FileBClass():

	def __init__(self):
	
		pass
		
	def functionB(self):
		changeThisText = "aaaaaaaaaaaaa"
		print("watch for changes - "+str(changeThisText))
		
def standaloneFunction():
	phrase = "bananas"
	print("changes? - "+str(phrase))
	
# --------------------

		if (mod_path.startswith('./') or mod_path.startswith(doc_path)):
			del sys.modules[name]
			
# --------------------

