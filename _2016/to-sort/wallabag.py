# http://myword.jeffreykishner.com/users/kishner/essays/003.html
# https://gist.github.com/jkishner/d6f324c405f53e9380ba#file-wallabag
# !/usr/bin/env python

# -*- coding: utf-8 -*-
# I am more than likely importing more libraries than are necessary
import urllib2 
import urllib 
import re 
import clipboard 
import urlparse 
import notification 
import webbrowser
import base64

# Grab url (or whatever) from the clipboard
u = clipboard.get()

# replace everything up to the ? with the URL of your wallabag installation
link = "YOURDOMAIN/wallabag/?action=add&autoclose=true&url="
link += base64.b64encode(u)
webbrowser.open(link)