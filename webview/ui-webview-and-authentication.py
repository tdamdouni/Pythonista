# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2517/ui-webview-and-authentication_

# coding: utf-8

import requests, ui

def basic_login_webview(url, username, password):
	webview = ui.WebView(name=url)
	webview.load_html(requests.get(url, auth=(username, password)).text)
	return webview
	
webview = basic_login_webview(url='https://my.favorite.url', username='xxx', password='yyy')
webview.present()

###

# @omz

import ui

v = ui.WebView()
v.load_url('http://user:passwd@httpbin.org/basic-auth/user/passwd')
v.present()

