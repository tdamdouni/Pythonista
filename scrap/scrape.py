#!python2
# coding: utf-8

# https://gist.github.com/jsbain/80cdc7dd82da23cbe16c9befef91d707

from __future__ import print_function
import ui,requests, json, time, console, urllib

# create debuggin delegate code. not necessary, but helpful for debugging
debugjs='''
// debug_utils.js
// 1) custom console object
console = new Object();
console.log = function(log) {
  // create then remove an iframe, to communicate with webview delegate
  var iframe = document.createElement("IFRAME");
  iframe.setAttribute("src", "ios-log:" + log);
  document.documentElement.appendChild(iframe);
  iframe.parentNode.removeChild(iframe);
  iframe = null;    
};
// TODO: give each log level an identifier in the log
console.debug = console.log;
console.info = console.log;
console.warn = console.log;
console.error = console.log;

window.onerror = (function(error, url, line,col,errorobj) {
   console.log("error: "+error+"%0Aurl:"+url+" line:"+line+"col:"+col+"stack:"+errorobj);})

console.log("logging activated");
'''


class debugDelegate (object):
    def webview_should_start_load(self,webview, url, nav_type):
        if url.startswith('ios-log'):
            print(urllib.unquote(url))
        print('should start:{}'.format(url))
        return True
        
    def webview_did_start_load(self,webview):
        print('did start')
        return True
    def webview_did_finish_load(self, webview):
        print('did finish')
        print(len(w.eval_js('document.documentElement.outerHTML')))
        pass
    def webview_did_fail_load(self, webview, error_code, error_msg):
        print('did fail {} {}'.format(error_code,error_msg))
        pass
# create webview, and turn on debugging delegate
w=ui.WebView()

w.delegate=debugDelegate()
w.eval_js(debugjs)
w.eval_js('console.log("before load");')
w.load_url('https://google.com')
w.eval_js('console.log("after load");')

