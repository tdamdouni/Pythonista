# startTimer.py - writes epoch time to text file for work log
#  by: Jason Verly
# rev date: 2014-07-25
import time
import console
import os
import os.path
import clipboard
import webbrowser
import urllib

if os.path.isfile('timer.txt'):
	console.clear()
	console.hud_alert('File exists', 'error')
	webbrowser.open('drafts4://')
	
else:
	console.clear()
	curDate = time.time()
	f = open('timer.txt', 'w')
	f.write(str(curDate))
	f.close()
	console.hud_alert('Timer started','success')
	
	worklogtext = clipboard.get()
	encodetxt = urllib.quote(worklogtext, safe='')
	draft_url = 'drafts://x-callback-url/create?text='
	action = '&action%3DWorkLog_Entry&afterSuccess%3DDelete'
	
	webbrowser.open(draft_url + encodetxt + action)

