# coding: utf-8

# QuickReminder 2.1 - see: http://jarrodwhaley.com/other-projects/geekery/

# https://gist.github.com/jbwhaley/4deac45790fa339b537a

# https://forum.omz-software.com/topic/466/quick-reminders-via-notification-center/8

# In Drafts, enter the text of your reminder on the first line. Hit 'return' twice, and then enter the amount of time in which you'd like to be reminded, in minutes, on the third line of the draft, fire the QuickReminder Action.

import sys
import time
import urllib
import notification
import console
import sound
import webbrowser

numArgs = len(sys.argv)

if numArgs == 1:
	console.alert('This script is meant to be run from Drafts.app. See' +
	' the docs for more info.')
elif numArgs > 1 and (sys.argv[2]) == '':
	url = 'drafts4://x-callback-url/create?text=' + urllib.quote_plus(sys.argv[1])
	console.alert('Please enter a time interval, in minutes, in the body of'
	' your draft.', 'Go back to Drafts?', 'Yes')
	webbrowser.open(url)
elif numArgs == 3:
	digit = sys.argv[2].replace(",", "")
	interval = int(digit) * 60
	text = sys.argv[1]
	notes = 'C3', 'D3', 'A3', 'B3'
	url = 'drafts4://x-callback-url/create?text=' + ''
	for note in notes:
		sound.play_effect('Piano_' + note)
		time.sleep(0.2)
	console.alert('Schedule?', 'Alert in' + ' ' + digit + ' ' +
	'minutes?', 'Schedule')
	notification.schedule(text, interval, 'default')
	webbrowser.open(url)
else:
	console.alert('Failed.')

