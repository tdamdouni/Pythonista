# https://gist.github.com/jsbain/045ec1b9a953e52778ca206bcc7c2898

# https://forum.omz-software.com/topic/3199/command-history

# here are some tools that can be used (e.g. from wrench menu) to save /load a command history session

from objc_util import UIApplication
with open('history.py','r') as f:	
	UIApplication.sharedApplication().keyWindow().rootViewController().accessoryViewController().consoleViewController().history=	f.readlines()
