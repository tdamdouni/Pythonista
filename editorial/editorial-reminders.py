# coding: utf-8

# @Editorial Workflow

# https://forum.omz-software.com/topic/2429/editorial-reminders/7

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

# --------------------

def extract_alarm_info(alarm_text):
    for name, s_time in re.findall(r'(.*)@alarm\((.*)\)', alarm_text):
        date, time = s_time.split(', ') 
        d_yyyy, d_mm, d_dd = [int(x) for x in date.split('-')]
        t_hh, t_mm = [int(x) for x in time.split(':')]
    
    return {
                'year'      : d_yyyy,
                'month'     : d_mm,
                'day'           : d_dd,
                'hour'      : t_hh,
                'min'           : t_mm,
                'date_str'  : date,
                'time_str'  : s_time,
            }

the_alarm = '@alarm(2015-12-10, 22:05)'
print(extract_alarm_info(the_alarm))

# --------------------

import datetime
the_alarm = '@alarm(2015-12-10, 22:05)'
alarm_datetime = datetime.datetime.strptime(the_alarm, '@alarm(%Y-%m-%d, %H:%M)')
print((alarm_datetime, str(alarm_datetime)))
# (datetime.datetime(2015, 12, 10, 22, 5), '2015-12-10 22:05:00')

# --------------------

import dateutil  # a builtin in the current Beta

# returns the substring that is inside of two delimiters
def str_inside(s, delimiters='()'):  # 'this (is a) test.' --> 'is a'
    return (s.partition(delimiters[0])[2] or s).partition(delimiters[1])[0]

the_alarm = '@alarm(2015-12-10, 22:05)'
alarm_datetime = dateutil.parser.parse(str_inside(the_alarm))
print((alarm_datetime, str(alarm_datetime)))

# --------------------

for s in '2/13/70', '8:00 on 13 Feb 70', "8am on 13th Feb 1970", 'July 4th', '7:30am', '7:30pm', 'Monday':
    print((dateutil.parser.parse(s), s))
# --------------------
