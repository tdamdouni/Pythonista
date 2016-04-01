# http://www.leancrew.com/all-this/2013/10/simple-expense-report-with-drafts-and-pythonista/
# coding: utf-8
# To call script from Drafts, use the following URL as URL Action:
# pythonista://total?action=run&argv=[[body]]&argv=[[title]]

import sys
import webbrowser
import urllib

raw = sys.argv[1].split('\n')
title = sys.argv[2]
cleaned = [title, '']
numbers = []

for line in raw:
  try:
    desc, cost = line.rsplit(None, 1)
    cost = float(cost.strip('$ '))
    numbers.append(cost)
    cleaned.append('{:<25}{:>10,.2f}'.format(desc, cost))
  except ValueError:
    cleaned.append(line)
total = sum(numbers)
while cleaned[-1].strip() == '':
  del cleaned[-1]
cleaned.append('')
cleaned.append('Total{:>30,.2f}'.format(total))
cleaned = '\n'.join(cleaned)

webbrowser.open("drafts4://x-callback-url/create?text=" + urllib.quote(cleaned))