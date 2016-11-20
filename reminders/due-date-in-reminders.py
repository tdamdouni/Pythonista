# https://forum.omz-software.com/topic/3525/bug-report-strange-due-date-in-reminders-module-in-gmt-9

import reminders, webbrowser
from datetime import datetime, timedelta

r = reminders.Reminder()
a = reminders.Alarm()
r.due_date = a.date = datetime.now().replace(hour=14)
r.alarms = [a]
r.title = 'GMT+9 Today 14:xx:xx'
r.save()

r = reminders.Reminder()
a = reminders.Alarm()
r.due_date = a.date = datetime.now().replace(hour=15)
r.alarms = [a]
r.title = 'GMT+9 Today 15:xx:xx'
r.save()

webbrowser.open('x-apple-reminder://')

# --------------------

import reminders, webbrowser
from datetime import datetime, timedelta

r = reminders.Reminder()
a = reminders.Alarm()
r.due_date = a.date = datetime.now().replace(hour=0)
r.alarms = [a]
r.title = 'GMT-4 Today 00:xx:xx'
r.save()

r = reminders.Reminder()
a = reminders.Alarm()
r.due_date = a.date = datetime.now().replace(hour=23)
r.alarms = [a]
r.title = 'GMT-4 Today 23:xx:xx'
r.save()

webbrowser.open('x-apple-reminder://')

# --------------------

