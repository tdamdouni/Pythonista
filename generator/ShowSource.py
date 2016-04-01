# http://mygeekdaddy.net/2014/09/22/a-better-way-to-view-page-sources-in-ios/
# coding: utf-8
import webbrowser
import sys

url = sys.argv[1]
path = sys.argv[2]

webbrowser.open('textastic://'+url+'/'+path)