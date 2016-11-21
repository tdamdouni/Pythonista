# coding: utf-8

# https://forum.omz-software.com/topic/2978/download-pdf-on-safari-and-open-in-pythonista-script/2

import appex
import os
import shutil

path = appex.get_url()[len("file://"):]
name = os.path.basename(path)
dest = os.path.join(os.path.expanduser("~/Documents"), name)
shutil.copy(path, dest)

# To convert the file: URL to a normal path, you can simply remove the file:// prefix using path = url[len("file://"):]. (You can of course just write path = url[7:], but it's not very obvious what the 7 means.)

# Pythonista's "Script Library" is located at ~/Documents. ~ is the "home" directory, to convert that to a normal path use os.path.expanduser("~/Documents").

# So if you want to save the file into Pythonista, you can use something like this:

#vThis could be condensed into less lines, I've split it up a little for clarity.

# Though if you just want to work with the PDF file and don't need to keep it permanently, you can open the path normally:

# with open(path, "rb"):
    # do whatever you need to

# @omz That won't work correctly if the URL contains percent escapes. A better method would be to use urlparse and urllib.url2pathname, like this:

# from urlparse import urlparse
# from urllib import url2pathname

# p = urlparse(file_url)
# file_path = url2pathname(p.path)

