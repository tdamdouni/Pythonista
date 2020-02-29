# coding: utf-8

# https://gist.github.com/wcaleb/2e6da75a4c91f8b46dd4

"""
This script ingests a CSV exported from Library Thing and
returns the percentage of author last names that begin with
each letter of the alphabet.

Based on original script by Andrew Pendleton for analyzing
U.S. Census data: https://gist.github.com/apendleton/2638865

"""
from __future__ import print_function

from csv import DictReader
from collections import defaultdict
import sys

def getitem(l, p, default=None):
	try:
		return l[p]
	except IndexError:
		return default
		
c = DictReader(open(getitem(sys.argv, 1, "LibraryThing_export.csv"), "rU"))
field = getitem(sys.argv, 2, "'AUTHOR (last, first)'")

data = defaultdict(int)
for row in c:
	first_letter = row[field][0].upper() if row[field] else None
	if (first_letter and first_letter.isalpha()):
		data[first_letter] += float(1)
		
# adjust to get actual percentages
total = sum(data.values())

out = {letter: (count / total) * 100 for letter, count in data.iteritems()}

for l in sorted(out, key=out.get, reverse=True):
	print(l + ' - ', "{0:.2f}".format(out[l]) + '%')

