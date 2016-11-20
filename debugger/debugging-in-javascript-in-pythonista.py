# https://forum.omz-software.com/topic/1804/debugging-in-javascript-in-pythonista 

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

// 2) custom onerror, which logs info about the error
   window.onerror = (function(error, url, line,col,errorobj) {
   console.log("error: "+error+"%0Aurl:"+url+" line:"+line+"col:"+col+"stack:"+errorobj);})

console.log("logging activated");

# --------------------

# coding: utf-8

import ui,os,urllib
class debugDelegate (object):
    def webview_should_start_load(self,webview, url, nav_type):
       if url.startswith('ios-log'):
          print urllib.unquote(url)
       return True
if __name__=='__main__':
   w=ui.WebView(frame=(0,0,576,576))
   w.delegate=debugDelegate()
   w.load_url(os.path.abspath('test_1.html'))
   w.present('sheet')

# --------------------

<html>
   <head>
      <title>Title</title>
         <script  src="debug_utils.js"></script>
         <script> function crash(){ return misspelledfcn();} </script>
   </head>

   <body>
   
   <h1>Hello</h1>
<button onclick="crash()">click me to cause an error</button>
<button onclick="console.log('hello world!')">click me to log a message</button>
   </body>

</html>

# --------------------
