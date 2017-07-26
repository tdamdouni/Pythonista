_Captured: 2016-12-25 at 16:13 from [m.linuxjournal.com](http://m.linuxjournal.com/content/tech-tip-really-simple-http-server-python)_

If you need a quick web server running and you don't want to mess with setting up apache or something similar, then Python can help. Python comes with a simple builtin HTTP server. With the help of this little HTTP server you can turn any directory in your system into your web server directory. The only thing you need to have installed is Python.

Practically speaking this is very useful to share files inside your local network. Implementing this tiny but hugely useful HTTP server is very simple, its just a single line command.

Assume that I would like to share the directory /home/hisam and my IP address is 192.168.1.2

Open up a terminal and type:

$ cd /home/somedir
$ python -m SimpleHTTPServer
That's it! Now your http server will start in port 8000. You will get the message:

Serving HTTP on 0.0.0.0 port 8000 ...
Now open a browser and type the following address:

http://192.168.1.2:8000
You can also access it via:

http://127.0.0.1:8000
If the directory has a file named index.html, that file will be served as the initial file. If there is no index.html, then the files in the directory will be listed.

If you wish to change the port that's used start the program via:

$ python -m SimpleHTTPServer 8080
If you want to only serve on localhost you'll need to write a custom Python program such as:

import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


HandlerClass = SimpleHTTPRequestHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
Note also that this should also work on Windows or Cygwin.
