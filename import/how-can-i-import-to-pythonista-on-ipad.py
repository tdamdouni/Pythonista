# coding: utf-8

# https://forum.omz-software.com/topic/3363/i-have-a-python-project-on-my-pc-how-can-i-import-to-pythonista-on-ipad/6

import requests
import appex
from console import alert, input_alert
import os.path
import os

def main():
	if not appex.is_running_extension():
		alert("Error", "This script is intended to be run from the sharing extension.", "Exit", hide_cancel_button=True)
		return
		
	url = appex.get_url()
	if not url:
		alert("ERROR", "No input URL found.  Execute this script from the sharing extension.", "Quit", hide_cancel_button=True)
		return
		
	root_path = "../../Documents/Downloads/"
	
	while True:
		filename = input_alert("Download File", "You have chosen to download file at URL:\n " + url + "\n\nEnter filename to save locally.  Press Cancel to abort.")
		filename = root_path+filename
		if os.path.exists(filename):
			if os.path.isfile(filename):
				confirm = alert("Warning", "File %s exists.  Overwrite?" % filename, "Overwrite", "Change Filename", hide_cancel_button=True)
				if confirm == 1:
					os.remove(filename)
					break
			else:
				alert("Critical Error.", "Path exists but is not a file.  Exiting.", "Exit", hide_cancel_button=True)
				return
		else:
			break
			
	r = requests.get(url)
	if r.status_code != 200:
		alert("Invalid HTTP Response: %d, Exiting." %r.status_code, "Exit", hide_cancel_button=True)
		return
		
	confirm = alert("Confirm Download", "Text length: %d, Press OK to Save, Cancel to Quit" %len(r.text), "Save", "Cancel", hide_cancel_button=True)
	if confirm == 1:
		outfile = open(filename, "w")
		for line in r.text:
			outfile.write(line)
		outfile.close()
		alert("Success", "File Saved.", "Exit", hide_cancel_button=True)
	r.close()
	return
	
	
if __name__ == '__main__':
	main()
	
# --------------------

