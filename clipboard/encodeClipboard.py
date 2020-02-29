# coding: utf-8
from __future__ import print_function
import clipboard
import urllib

s = clipboard.get()

s = s.encode('utf-8')
s = urllib.quote(s, safe='')

print(s)

