# coding: utf-8

# https://gist.github.com/jsbain/bbd5ef7e2e4010a631bd

from objc_util import *
app=UIApplication.sharedApplication()
rootVC = app.keyWindow().rootViewController()
tabVC = rootVC.detailViewController()
tvc=tabVC.selectedTabViewController()
ed=tvc.editorView()
tv=ed.textView()
tv.showLineNumbers=not tv.showLineNumbers()
if tv.gutterView():
	tv.gutterView().backgroundColor=tv.backgroundColor()
	tv.gutterWidth=20 #adjust per preference.  35 is default
#not sure how to force a redraw.  changing frame size works
oldframe=tv.frame()
newframe=oldframe
newframe.size.width-=1
tv.frame=newframe
import time
time.sleep(0.1)
tv.frame=oldframe
