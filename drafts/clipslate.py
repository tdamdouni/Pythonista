# -*- coding: utf-8 -*-
"""
clipslate.py: capture page title and url and current 
iOS system clipboard and append to a notesy.app file 
in markdown format in order to collect a series of dated,
named and linked pieces of copied plain text for 
later processing
notsey.app x-callback-url implementation is documented at http://notesy-app.com/weblog/files/b7e15801e5b4448495eaaccfdb374cc7-20.htm
This script can be adapted for any other x-callback-url app with an append action
2013-04-27
(c) 2013 Richard Careaga, all rights reserved.
Subject to license terms and conditions at
http://richard-careaga.com/lic2013.txt

adapted from clip2poster
(http://omz-software.com/pythonista/forums/discussion/190/posting-to-wordpress-from-safari-with-clipboard)

install this script to your pythonista.app top-level directory

Create the following bookmark in your browser app with the name
'cs' (or your choice):

    javascript:window.location='pythonista://clipslate?action=run&argv='+encodeURIComponent(document.title)+'&argv='+encodeURIComponent(location.href);

Then navigate to target page, highlight some text, copy it and tap the cs bookmark

Known bug: does not handle unicode characters

Known limitation: system clipboard copies plain text from browsers, not HTML, so copied embedded limks are lost

"""

import sys
import clipboard
import urllib
import webbrowser
from datetime import datetime

# convenience definitions

bq = '> '
colonspace = ': '
nl = '\n'
ruler = '---'
spacer = '\n\n'
slate = "slate.txt" # change to suit
today = datetime.today()
the_date = today.strftime('%Y-%m-%d')

# convenience functions

def bracket(s):
	return '[' + s + ']'

def accessed():
	return ' on ' + the_date

def blockquote():
	return bq + the_clip

# clip is from the system clipboard
# if you highlighted text but did not also copy it
# what will show up is the last item that was 
# copied or cut in any application in which you
# might have been working before

the_clip = clipboard.get()

# sys.argv[0] = this appname
# sys.argv[1] = the webpage title
# sys.argv[2] = the webpage url

the_title = sys.argv[1]
the_url = sys.argv[2]

# layout and format in markdown

first_line = 'Clipped from ' + bracket(the_title) + accessed()
link = bracket(the_title) + colonspace + the_url

payload = first_line + spacer + blockquote() + spacer + link + spacer + ruler + spacer

# copy the completed formatted clipping onto the system clipboard

clipboard.set(payload)

# construct the x-callback url
target = 'drafts4://x-callback-url/append?name=' + slate

# append the reloaded clipboard to append to the specified
# notesy file

webbrowser.open(target)