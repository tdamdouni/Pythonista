# coding: utf-8

# https://forum.omz-software.com/topic/3004/auto-fill-form-and-simulate-enter/9

# 
#!python2
# coding: utf-8
from __future__ import print_function
import ui,requests, json, time, console, urllib
debug=False
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
        return True
        
# create webview, and turn on debugging delegate
w=ui.WebView()

if debug:
    w.delegate=debugDelegate()
    w.eval_js(debugjs)

# load page
print('loading page')
w.load_url('http://webpagetopdf.com')

# wait for documentState to start loading, 
for i in range(10):
    if w.eval_js('document.readyState')!='complete':
        break
    time.sleep(1)
# ...then wait for it to complete
while w.eval_js('document.readyState')!='complete':
    time.sleep(1)

# fill in form, and click button
w.eval_js('url=document.getElementById("url");')
w.eval_js('url.value="www.google.com";')
w.eval_js('btn=document.getElementById("start-button");')
print('clicking button, and waiting for response')
w.eval_js('btn.click()')

# wait until downloadlink is populated, then grab link.  TODO: Timeout
while json.loads(w.eval_js('document.getElementsByClassName("download-link").length<1')):
    time.sleep(0.5)
link=w.eval_js('document.getElementsByClassName("download-link")[0].href')

# download
print(link)
r=requests.get(link)
with open('webpage.pdf','wb') as f:
    f.write(r.content)
print('download complete') 
