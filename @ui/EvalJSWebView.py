# coding: utf-8

# https://forum.omz-software.com/topic/2792/webview-bug

import ui
from objc_util import ObjCInstance, on_main_thread

web_view = ui.WebView(frame=(0,0,500,500))
web_view.present('sheet')
web_view.load_url('https://www.google.com')

js = 'alert(document.title)'
wv = ObjCInstance(web_view).subviews()[0]
on_main_thread(wv.stringByEvaluatingJavaScriptFromString_)(js)