# coding: utf-8

# https://forum.omz-software.com/topic/2529/how-to-load-a-local-gif-into-ui-webview

# You can construct a file:// URL from the image path, and load it using load_url:

import urlparse
import urllib
import os
import ui

# Change this:
img_path = os.path.abspath('Examples/Misc/animation.gif')

img_url = urlparse.urljoin('file:', urllib.pathname2url(img_path))

webview = ui.WebView()
webview.load_url(img_url)
webview.present()
