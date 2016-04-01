# I got help from here: http://twolivesleft.com/Codea/Talk/discussion/1652/what-others-do%3A-pythonista/p1
# I got help from here: http://www.macdrifter.com/2012/09/pythonista-trick-url-to-markdown.html
# I got help from here: http://www.macstories.net/tutorials/from-instapaper-and-pythonista-to-dropbox-and-evernote-as-pdf/

import sys
import urllib2
import editor
import os

url = sys.argv[1]
scriptName = os.path.basename(url)
contents = urllib2.urlopen(url).read()
editor.make_new_file(scriptName[:-3], contents)
