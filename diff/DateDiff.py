from __future__ import print_function
# Daviesia
# Program to calculate the days between two dates.
# Author: Ian D. Davies
# Date: October 8, 2014
# **DateDiff.py** - Use date arithmetic to show days between to dates.---------------------------------------------------------------------
import datetime

today = datetime.date.today()
SomeDate = datetime.date(2016, 01, 28)
diff = today - SomeDate
# print 'Somedate is', diff.days, 'day(s) away'
print('Ihr Geburtstag liegt', diff.days, 'Tage her')
