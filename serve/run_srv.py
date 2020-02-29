# https://gist.github.com/schimfim/5153629

'''
Run current script as web application.

When run from the editor action menu,
this script will take the file currently
open in the editor and run it as a
request handler for an HTTPServer. The
file must define a class "Handler" as
a subclass of BaseHTTPRequestHandler to
handle the requests (see example below).
After starting the server, it is
accessed using the built-in webbrowser.

Installation: Put this script in the 
editor action menu.

For more info, see the documentation for
built-in module BaseHTTPServer.
As a simple example, copy the following
code to a new script and run 'run_srv'
from the actions menu. It uses
SimpleHTTPRequestHandler, which is a
subclass of BaseHTTPRequestHandler.

from SimpleHTTPServer import SimpleHTTPRequestHandler
Handler = SimpleHTTPRequestHandler
'''
from __future__ import print_function

from BaseHTTPServer import HTTPServer
import webbrowser
import editor

p = editor.get_text()
exec(p)
if 'Handler' in locals():
	httpd = HTTPServer(("", 8000), Handler)
	webbrowser.open('http://localhost:8000', stop_when_done = True)
	httpd.serve_forever()
else:
	print('No class "Handler" found')