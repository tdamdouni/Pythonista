# https://forum.omz-software.com/topic/3972/taskpaper-and-reminders-recurring-tasks

import reminders
todo = reminders.get_reminders(completed=False)
print('TODO List')
print('=========')
for r in todo:
	#print('[ ] ' + r.title)
	print('[ ] {} {}'.format(r.title, r.due_date))
done = reminders.get_reminders(completed=True)
print('DONE')
print('====')
for r in done:
	#print('[x] ' + r.title)
	print('[x] {} {}'.format(r.title, r.due_date))

