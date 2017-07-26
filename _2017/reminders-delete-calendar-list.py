# https://forum.omz-software.com/topic/4081/reminders-delete-calendar-list/5

import reminders

try:  # https://docs.python.org/3/whatsnew/3.0.html#builtins
    raw_input          # Python 2
except NameError:
    raw_input = input  # Python 3

print('=' * 25)

c = reminders.Calendar()
c.title = "Delete Me!!!"
c.save()
print(c)

while True:
    calendars = reminders.get_all_calendars()
    for i, calendar in enumerate(calendars):
        print(i, calendar)
    i = int(raw_input('Enter number of the calendar to delete ("q" to quit): ').strip())
    print('({}): {}'.format(type(i), i))
    print('({}): {}'.format(type(calendars[i]), calendars[i]))
    print(reminders.delete_calendar)
    reminders.delete_calendar(calendars[i])