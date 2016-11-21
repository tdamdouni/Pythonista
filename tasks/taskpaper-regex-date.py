# coding: utf-8

# https://forum.omz-software.com/topic/2971/taskpaper-worklfows-for-regex-matching-past-and-today-s-date/2

import datetime

tag = 'start'
today = datetime.date.today()

data = '''
No tag goes nowhere
@start() empty tag goes nowhere
An old task @start(1970-02-13) goes in the past
Today's task goes in the present @start({:%Y-%m-%d})
A future task@start(  2059-11-20 )goes in the future
A slash-based date @start(2001/01/01) goes nowhere
'''.format(today)

print(data)

def get_past_present_and_future(data=data, tag='start'):
	at_tag = '@{}('.format(tag)
	past, present, future = [], [], []
	for line in data.splitlines():
		task_date = line.partition(at_tag)[2].partition(')')[0].strip()
		if task_date and task_date.count('-') == 2:
			task_date = datetime.datetime.strptime(task_date, '%Y-%m-%d').date()
			if task_date < today:
				past.append(line)
			elif task_date == today:
				present.append(line)
			else:
				future.append(line)
	return tuple(past), tuple(present), tuple(future)
	
print(get_past_present_and_future(data, 'start'))

# My point was that perhaps you were overthinking this use case. Regex and the entire first script are not required to effectively solve the problem at hand. This is because your data is so "well formed" that a single line of Python can isolate the date as a string (task_date = line.partition(at_tag)[2].partition(')')[0].strip()) and another line (task_date = datetime.datetime.strptime(task_date, '%Y-%m-%d').date()) can convert that string into a datetime.date that can be trivially compared to datetime.date.today() to determine if this task is in the past, present, or future.

# My code above shows that your second and third scripts could find past and present tasks merely by looking for task-date <= today. No regex required, no first script, and no artificial 15 year limit.

# EDIT: As I think about it more, given that your dates are already in year-month-day sort order, you do not even need to convert them to dates... You can just leave them as strings and do string compares with today's date as a string.

