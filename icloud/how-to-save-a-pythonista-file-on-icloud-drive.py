# https://forum.omz-software.com/topic/3264/how-to-save-a-pythonista-file-on-icloud-drive

# https://workflow.is/workflows/02454139a4ac4f3da3005919c978ea81

import webbrowser
import clipboard
filename = 'your file'
#... save your file into Dropbox, for instance in a folder named Pythonista,
#... via a script you find easyly in these forums
clipboard.set(filename)
webbrowser.open('workflow://run-workflow?name=SavePythonistaFileInIcloudDrive&input=clipboard')

