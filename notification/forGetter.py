#!/usr/bin/python
# -*- coding: utf-8 -*-

# forGetter Version 1.1

## A simple script to view all system notifications scheduled by Pythonista.
## Currently running it from Launch Center Pro.

import notification
import console
import datetime
import webbrowser

# Global variables

header = "Scheduled Notifications\n"
scheduled = notification.get_scheduled()
output_list = []
url = 'launch://'

# Run the logic

if scheduled == []:
	console.hud_alert('None.', 'error')
else:
	for i in scheduled:
		ms = i[u'message']
		ts = i[u'fire_date']
		ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		item = ms + ":\n" + ts + "\n"
		output_list.append(item)
	output_string = "\n".join(output_list)
	console.alert(header, output_string, 'Dismiss?', hide_cancel_button=True)
	
webbrowser.open(url)

