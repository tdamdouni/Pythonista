# coding: utf-8
import clipboard
import urllib2
import webbrowser

clipString = clipboard.get()

marky = 'http://heckyesmarkdown.com/go/?u='

queryString = marky + clipString

reqMD = urllib2.Request(queryString)
openMD = urllib2.urlopen(reqMD)
content = (openMD.read().decode('utf-8'))
clipboard.set(content)

webbrowser.open(queryString)