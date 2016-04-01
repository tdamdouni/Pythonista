# coding: utf-8

# https://forum.omz-software.com/topic/2429/editorial-reminders/8

# I was listening to a podcast today where someone was raving about dateutil's ability to parse datetimes without format string. Given that dateutil is one of the Pythonista extra modules, I thought I would give it a whirl...

import dateutil  # a builtin in the current Beta

# returns the substring that is inside of two delimiters
def str_inside(s, delimiters='()'):  # 'this (is a) test.' --> 'is a'
    return (s.partition(delimiters[0])[2] or s).partition(delimiters[1])[0]

the_alarm = '@alarm(2015-12-10, 22:05)'
alarm_datetime = dateutil.parser.parse(str_inside(the_alarm))
print(alarm_datetime, str(alarm_datetime))

# dateutil.parser.parse() does not require a format string and is much better than strptime() at figuring out what datetime the user meant:

for s in '2/13/70', '8:00 on 13 Feb 70', "8am on 13th Feb 1970", 'July 4th', '7:30am', '7:30pm', 'Monday':
    print(dateutil.parser.parse(s), s)