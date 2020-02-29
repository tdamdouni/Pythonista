# coding: utf-8

# TaskpaperReminders Workflow

# https://forum.omz-software.com/topic/2429/editorial-reminders

# http://www.editorial-workflows.com/workflow/5795082133307392/HvLjGvUL-rE

# Assuming the alarm format is:
# name of alarm @alarm(yyyy-mm-dd, HH:MM)
# Then create a new workflow with the two items.
# First One is the get document text element
# Second one is to run the python code:

from __future__ import print_function
import re
import editor
import dialogs
import datetime
import workflow
import reminders

action_in = workflow.get_input()
for line in action_in.split('\n'):
	for name, s_time in re.findall(r'(.*)@alarm\((.*)\)', line):
		date, time = s_time.split(', ')
		d_yyyy, d_mm, d_dd = [int(x) for x in date.split('-')]
		t_hh, t_mm = [int(x) for x in time.split(':')]
		rem = reminders.Reminder()
		rem.title = name
		due = datetime.datetime(d_yyyy, d_mm, d_dd, t_hh, t_mm)
		rem.due_date = due
		a = reminders.Alarm()
		a.date = due
		rem.alarms = [a]
		try:
			res = dialogs.alert(
			'The Reminder Was Set',
			'Name: {name}\n{date} {time}'.format(
			name=name,
			date=date,
			time=time),
			'Ok')
			rem.save()
		except KeyboardInterrupt:
			print("User Cancled Input")
			
			
action_out = action_in

workflow.set_output(action_out)

