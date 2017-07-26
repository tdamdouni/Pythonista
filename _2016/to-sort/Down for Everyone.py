# -*- coding: utf-8 -*-
# Checks Down for Everyone
# to see if the URL in your
# clipboard is up and running
#
# By Jake Bilbrey
# http://jakebilbrey.com
#
# Edited by Edi Venturin
# http://ediventurin.com
# added possibility to get URL from bookmarklet
#
# Bookmarklet to be added in Mobile Safari:
# javascript:window.location='pythonista://DownForEveryone?action=run&argv='+encodeURIComponent(location.href);
#
import console
import clipboard
import urllib
import bs4
import webbrowser
import re

try:
    if (clipboard.get()).find("http") >= 0:
    	website = clipboard.get()
    else:
	numArgs = len(sys.argv)
	if numArgs == 2:
		website = sys.argv[1]
	else:
		website = console.input_alert("Down for Everyone?","Insert a URL")

    check = bs4.BeautifulSoup(urllib.urlopen("http://www.isup.me/" + website))
    checkStr = check.find_all(text=re.compile("It's just you."))

    if checkStr:
    	console.alert("It is up!",website)
    else:
    	console.alert("It is down!",website)
except:
	console.clear()
