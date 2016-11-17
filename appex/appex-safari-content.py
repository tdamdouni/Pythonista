# https://forum.omz-software.com/topic/2358/appex-safari-content

# coding: utf-8
import urllib2, appex
response = urllib2.urlopen(appex.get_url()')
html = response.read()