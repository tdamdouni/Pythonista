# coding: utf-8

# To call script from Drafts, use the follwing URL as URL Action:
# <pythonista://list.py?action=run&argv=[[draft]]>

# https://gist.github.com/hiilppp/7884176

# Python script to manipulate text in Pythonista in the following manner and send the result (back) to Drafts: Sort lines, remove blank and duplicate lines, and prepend a hyphen to lines which don't start with one.

import os
import re
import sys
import urllib
import webbrowser

a = re.sub(r"(?m)^[*-] ", "", sys.argv[1])

a = set(a.split("\n"))
a = "".join([l + "\n" for l in a])

a = os.linesep.join([s for s in a.split("\n") if s])

a = a.split("\n")
a.sort(key=str.lower)
a = "\n".join(a)

a = re.sub(r"(?m)^", "- ", a)

webbrowser.open("drafts4://x-callback-url/create?text=" + urllib.quote(a))