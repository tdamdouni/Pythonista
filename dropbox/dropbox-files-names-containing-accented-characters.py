# coding: utf-8

# https://forum.omz-software.com/topic/3094/dropbox-files-names-containing-accented-characters/6

# --------------------

from __future__ import print_function
url = unicode(urllib.unquote(url), 'utf-8')

# --------------------

url = urllib.unquote(url).decode('utf-8')

# --------------------

# coding: utf-8

import urllib
import appex

#url = 'https://www.dropbox.com/s/5mmxh7h7vu2lwnp/La%20vie%20tr%C3%A8s%20priv%C3%A9e%20de%20Monsieur%20Sim.png?dl=0'
url = appex.get_url()
print(url)
print(urllib.unquote(url).decode('utf-8'))

# -----

import urllib

# This is a unicode string literal (note the 'u' before the quotes), to simulate the behavior of appex.get_url():
url = u'https://www.dropbox.com/s/5mmxh7h7vu2lwnp/La%20vie%20tr%C3%A8s%20priv%C3%A9e%20de%20Monsieur%20Sim.png'
print(urllib.unquote(url.encode('utf-8')).decode('utf-8'))

# --------------------

