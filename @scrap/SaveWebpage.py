# coding: utf-8

# https://forum.omz-software.com/topic/2450/save-webpage-for-offline

import urllib2
page = urllib2.urlopen("http://amdouni.com")
with open("out.html", "w") as outfile:
    outfile.write(page.read())

# You can load the contents of this file into a WebView now. I don't know if load_url supports local files, but you can always use load_html. This will load the file we saved in the last example into a ui.WebView

import ui
with open("out.html", "r") as outfile:
    html = outfile.read()

wv = ui.WebView()
wv.load_html(html)
wv.present()

# If you don't need to access the HTML between two separate runnings of the script, you don't have to save the file and then read it again, you can just store it locally.