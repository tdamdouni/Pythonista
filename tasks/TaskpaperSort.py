#!/usr/bin/env python

# https://gist.github.com/derickfay/8891099
# http://dfay.fastmail.fm/et/
from __future__ import print_function
import re
import sys

# first & only argument is the text to be parsed
theText = sys.argv[1]

theList=[]
j=""

for i in theText.splitlines():
	match = re.search('@due\(\d\d\d\d\-\d\d\-\d\d\)',i)
	if match:
		theKey = i[i.find('@due(')+5:i.find('@due(')+15]
	else:
		theKey =''
	theList = theList + [(theKey, i)]

for i in sorted(theList):
		j = j+i[1]+"\n"

j = j[:-1]
print(j)