# coding: utf-8

# https://gist.github.com/hiilppp/9936000

# Pythonista script that randomly selects a reminder (out of a given list) and schedules a (quiet) notification for that reminder at a random point of time in the future (within a given range). Opening the notification will then schedule a new reminder notification (and, if provided, follow a link).

import notification
from random import randint
import sys
import urllib
import webbrowser

reminders = ["Reminder A", ["Reminder B", "url://"], "Reminder C"]

n = randint(0, len(reminders)-1)
URL = "pythonista://random_reminders.py?action=run"

if type(reminders[n]) == list:
	random_reminder = reminders[n][0]
	URL = URL + "&argv=" + urllib.quote(reminders[n][1], safe = "")
else:
	random_reminder = reminders[n]

d = 60*60*24
random_delay = randint(d, 7*d)

notification.schedule(random_reminder, random_delay, "", URL)

try:
	webbrowser.open(sys.argv[1])
except:
	pass