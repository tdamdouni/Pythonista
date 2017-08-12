# Debugging in JavaScript in pythonista

_Captured: 2016-02-16 at 01:33 from [forum.omz-software.com](https://forum.omz-software.com/topic/1804/debugging-in-javascript-in-pythonista)_

been playing around in JavaScript again in pythonista. maybe I'm just smarter now, or maybe recent iOS versions have better safari capabilities....but I figured out some useful debugging features that make javascript tolerable. thinking of creating something like a developer tools view like you'd have in ie or chrome on the desktop... at minimum an interactive console, maybe watch window, etc.

    1. create a custom console.log, and window.onerror which enables logging and error reporting back to pythonista.
    
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
    

    1. on the webview side, you need a custom delegate to handle these log messages:
    
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
    

here I'm printing to console, but this could just as easily get printed to a scrolling TextView element, etc.

as an example of how this all works, here is test_1.html:
    
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
    
