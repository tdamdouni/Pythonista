# coding: utf-8

# https://forum.omz-software.com/topic/2739/strange-error-with-ui-webview/6

import ui
import urllib2
import re

v = ui.load_view()
v.present('sheet')
webview = ui.WebView

def main():
	fx = open('sites.txt', 'r')
	lines = fx.readlines()
	fx.close()
	link1 = re.split('/\n', lines[0])
	link1.pop()
	link2 = re.split('/\n', lines[1])
	link2.pop()
	link3 = re.split('/\n', lines[2])
	link3.pop()
	webview.load_url(link1)
	webview.present()
	
main()


#==============================

# coding: utf-8

import ui
import urllib2
import re

v = ui.load_view()
webview = ui.WebView()
webview.flex = 'WH'
v.add_subview(webview)
v.present('full_screen')

def main():
	fx = open('sites.txt', 'r')
	lines = fx.readlines()
	fx.close()
	link1 = lines[0].strip()
	#link1 = re.split('/\n', lines[0])
	#link1.pop()
	#link2 = re.split('/\n', lines[1])
	#link2.pop()
	#link3 = re.split('/\n', lines[2])
	#link3.pop()
	webview.load_url(link1)
	#webview.present() #if you don't need a second view!?
	
main()

#==============================

webview = ui.WebView(frame=(20,20,400,300))

#==============================

v = ui.load_view()
#webview = ui.WebView(frame=(20,20,400,300))
#webview.flex = 'WH'
#v.add_subview(webview)
v.present('sheet')
webview = v['webview1']

