# https://forum.omz-software.com/topic/3267/how-to-get-a-text-file-from-icloud-drive

# https://workflow.is/workflows/c4586ece09d9476588db013798785f87

import webbrowser
import clipboard
import time

# Get a text file from iCloud Drive via File Picker
def get():
	clipboard.set('')
	webbrowser.open('workflow://x-callback-url/run-workflow?name=GetFileFromIcloudDrive&x-success=pythonista://')
	text = clipboard.get()
	while text.find('GetFileFromIcloudDrive') < 0:
		text = clipboard.get()
		time.sleep(0.3)
		# Clipboard should be formatted as:
		#   GetFileFromIcloudDrive:filename.ext\n
		#   file_content
		i = text.find('\n')
		if i > 0:
			line1 = text[0:i]
			filename = line1[len('GetFileFromIcloudDrive:'):]
			print('/'+filename+'/')
			file = text[i+1:]
			locfil = open(filename,'w')
			locfil.write(file)
			locfil.close()
			
get()
# --------------------

