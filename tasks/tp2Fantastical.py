# https://gist.github.com/derickfay/10012120
# coding: utf-8
# tp2fantastical.py
#
# by Derick Fay, 2014-04-06
#
# an adaptation of the Selection to Fantastical Editorial workflow 
# (http://editorial-app.appspot.com/workflow/6172238982152192/Y3VYajI3Hzc ) 
# for use with Drafts and Pythonista (both required)
#
# works on iPhone and iPad
# I have also written an equivalent script for TaskPaper for the Mac
# available at http://www.hogbaysoftware.com/wiki/ParseClipboardInFantastical
#
# installation: 
# 1) copy this script into Pythonista and name it tp2fantastical
# 2) create a Drafts URL Action with the following URL:
# pythonista://tp2fantastical?action=run&argv=[[draft]]

# Sends the input text to Fantastical, converting TaskPaper @due(YYYY-MM-DD) tags to plain text for Fantastical to parse as a Reminder. Designed for use with Drafts and Pythonista.

import sys
import webbrowser
import urllib
 
i = sys.argv[1]
#i = "Test item @due(2014-05-14)"
 
if '@due(' in i:
	theEnd=""
	theStart=i.split('@due(')[0]
	theDate=i.split('@due(')[1][0:10]
	theEnd=i[(i.index('@due(')+16):]
	i = theStart + " due " + theDate + theEnd
 
webbrowser.open("fantastical2://parse?sentence=" + urllib.quote(i))