#!/usr/bin/python
# -*- coding: utf-8 -*-

# CancelReminders Version 1.0

## Cancels all currently scheduled notifications in Pythonista.

import notification
import console
import webbrowser

scheduled = notification.get_scheduled()
url = 'launch://'

if scheduled == []:
	console.hud_alert('None.', 'error')
else:
	console.alert('Cancel all reminders?', 'Are you sure?', 'Yes')
	notification.cancel_all()
	console.hud_alert('Canceled.', 'success')
	
webbrowser.open(url)
