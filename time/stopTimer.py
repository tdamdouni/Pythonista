# stopTimer.py - generates closure notes for Drafts action
# & removes the temporary 'timer.txt' file
# by: Jason Verly
# rev date: 2014-07-25
import time
import console
import os
import os.path
import webbrowser
import clipboard
import urllib

if os.path.isfile('timer.txt'):
	console.clear()
	f = open('timer.txt', 'r+')
	s = f.read()
	a=float(s)
	curDate = time.time()
	diffDate = str(round((curDate - a)/60))
	endDate = time.strftime('%Y-%m-%d %I:%M %p', time.localtime(curDate))
	
	text = 'Task stopped at ' + endDate + '\n' + 'Total task duration: ' + diffDate + '\n————————————————————'
	
	clipboard.set(text)
	
	encodetxt = urllib.quote(text, safe='')
	draft_url = 'drafts://x-callback-url/create?text='
	action = '&action=WorkLog%20Closure'
	
	os.remove('timer.txt')
	
	webbrowser.open(draft_url + encodetxt + action)
	
else:
	console.clear()
	console.hud_alert('Timer not started', 'error')
	webbrowser.open('drafts://')

