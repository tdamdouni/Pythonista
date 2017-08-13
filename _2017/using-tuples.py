# https://forum.omz-software.com/topic/1239/extracting-the-date-from-the-ui-date-and-time-spinner/28

from collections import namedtuple

fields = ('year', 'month', 'day', 'text')
note = namedtuple('note', fields)

notes = [note(2017, 8, 11, 'yesterday'),
         note(2017, 8, 12, 'today'),
         note(2017, 8, 13, 'tomorrow')]

fmt = '{:<10} {:<10} {:<10} {}'
print(fmt.format(*fields))
for n in notes:
    print(fmt.format(*n))

"""
year       month      day        text
2017       8          11         yesterday
2017       8          12         today
2017       8          13         tomorrow
"""
