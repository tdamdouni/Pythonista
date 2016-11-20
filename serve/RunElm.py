# coding: utf-8

# https://gist.github.com/maxfell/3df8331a1de3a2dcd44face2089cad08

# https://twitter.com/maxfell/status/740661503263703041

# Compile Elm Code to JavaScript in Pythonista using Elm's web REPL

import appex
import requests
from bottle import route, run
from objc_util import *

SFSafariViewController = ObjCClass('SFSafariViewController')

@on_main_thread
def open_in_safari_vc(url, tint_color=None):
	vc = SFSafariViewController.alloc().initWithURL_entersReaderIfAvailable_(nsurl(url), True)
	app = UIApplication.sharedApplication()
	
	if app.keyWindow():
		window = app.keyWindow()
	else:
		window = app.windows().firstObject()
		
	root_vc = window.rootViewController()
	
	while root_vc.presentedViewController():
		root_vc
		root_vc.presentedViewController()
		
	root_vc.presentViewController_animated_completion_(vc, True, None)
	vc.release()
	
text = open(appex.get_file_path(), "r").read()

req = requests.request("POST", "http://elm-lang.org/compile", data={"input": text})

@route('/')
def present():
	return req.text
	
open_in_safari_vc("http://localhost:1337/")

run(host='localhost', port=1337, debug=True)

