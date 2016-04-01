# https://gist.github.com/anonymous/2a520253d378f3bd1d77

# This will create a new python script from the clipboard.  The 

import editor
import clipboard
import webbrowser
import os
import time
import sys


time.sleep(1)
editor.make_new_file(sys.argv[1], clipboard.get())
time.sleep(1)
execfile(sys.argv[1]+'.py')
time.sleep(1)
os.remove(sys.argv[1]+".py")
time.sleep(1)
webbrowser.open('workflow://')
time.sleep(1)