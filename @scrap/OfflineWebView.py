# coding: utf-8

# See:  https://forum.omz-software.com/topic/2450/save-webpage-for-offline

# https://github.com/cclauss/Pythonista_ui/blob/master/OfflineWebView.py

import requests, ui

url = 'https://en.m.wikipedia.org/wiki/Python_(programming_language)'
filename = (url.rpartition('/')[2] or url) + '.html'

try:
    html = requests.get(url).content
except requests.ConnectionError:
    html = ''

if html:
    with open(filename, 'w') as out_file:
        out_file.write(html)
else:
    try:
        with open(filename) as in_file:
            html = in_file.read()
    except IOError:  # file not found
        html = 'No connection to Wikipedia and article not found in local cache.'

web_view = ui.WebView()
web_view.load_html(html)
web_view.present()