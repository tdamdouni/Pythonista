# coding: utf-8

# https://forum.omz-software.com/topic/2429/editorial-reminders/4

import datetime
the_alarm = '@alarm(2015-12-11, 12:00)'
alarm_datetime = datetime.datetime.strptime(the_alarm, '@alarm(%Y-%m-%d, %H:%M)')
print(alarm_datetime, str(alarm_datetime))
# (datetime