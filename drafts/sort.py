# coding: utf-8

# To call script from Drafts, use the follwing URL as URL Action:
# <pythonista://sort?action=run&argv=[[draft]]>

# https://gist.github.com/hiilppp/6139407

# Python script to sort lines of text in Pythonista and send them (back) to Drafts.

# Cf. "Sorting with Pythonista" by @drdrang: http://www.leancrew.com/all-this/2013/08/sorting-with-pythonista/

import sys
import urllib
import webbrowser

a = sys.argv[1].split("\n")
a.sort(key=str.lower)
a = "\n".join(a)

webbrowser.open("drafts4://x-callback-url/create?text=" + urllib.quote(a))