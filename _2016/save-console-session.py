# https://forum.omz-software.com/topic/3902/sorry-if-this-is-obvious-but-is-there-an-easy-way-to-export-everything-in-the-shell-console-to-a-text-file/2

from objc_util import UIApplication
from time import ctime
# save history
with open('history.py','a') as f:
	f.write(ctime()+'\n')
	f.write(    '\n'.join([str(h) for h in
	UIApplication.sharedApplication().keyWindow().
	rootViewController().accessoryViewController().
	consoleViewController().history()
	])+'\n')
#save console output
with open('console_history.txt','w')    as f:
	f.write(ctime()+'\n')
	f.write(str(
	UIApplication.sharedApplication().
	keyWindow().rootViewController().
	accessoryViewController().consoleViewController().
	consoleOutputTextView().text()
	))

