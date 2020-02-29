from __future__ import print_function
# @scarp @web @JavaScript

# https://forum.omz-software.com/topic/2358/appex-safari-content/6

# coding: utf-8

jslogging='''
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

// 2) custom onerror, which logs info about the error
   window.onerror = (function(error, url, line,col,errorobj) {
   console.log("error: "+error+"%0Aurl:"+url+" line:"+line+"col:"+col+"stack:"+errorobj);})

console.log("logging activated");
'''

# coding: utf-8
import ui,os,urllib
class debugDelegate (object):
    def webview_should_start_load(self,webview, url, nav_type):
       if url.startswith('ios-log'):
          print(urllib.unquote(url))
       else:
          print(url)
       return True
w=ui.WebView()
w.eval_js(jslogging)


w.delegate=debugDelegate()

w.load_url('http://lab.pipwerks.com/javascript/cross-domain-iframes/')
#print source
w.eval_js('console.log(document.documentElement.outerHTML)')