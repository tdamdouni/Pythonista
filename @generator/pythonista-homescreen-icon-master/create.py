import editor
import makeicon
import base64
import clipboard
import console
import urllib
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import webbrowser
import os
import io
from threading import Timer
import sys
import re
reload(makeicon)

topcolor = tuple(int(i) for i in sys.argv[1].split(','))
bottomcolor = tuple(int(i) for i in sys.argv[2].split(','))
iconname = sys.argv[3]

# fix unicode error.
sys.stderr = io.BytesIO()

def getfilepath():
	abspath = editor.get_path()
	if abspath:
		return abspath.split('/Documents/')[1]
	else: 
		return console.input_alert('Path to the script (e.g. apps/foo.py):')

console.show_activity('Creating icon...')

icon, poster = makeicon.makeimages(topcolor, bottomcolor, iconname)

with open('template.html') as f:
	html = f.read()
html = html.replace('{{{URL}}}', 'pythonista://'+urllib.quote(getfilepath())+'?action=run')
html = html.replace('{{{ICON}}}', 'data:image/png;base64,'+base64.b64encode(icon.to_png()))
html = html.replace('{{{POSTER}}}', 'data:image/png;base64,'+base64.b64encode(poster.to_png()))
html = html.replace('{{{NAME}}}', re.match(r'.*/([^/]*)\.py.*', editor.get_path()).group(1))

b64 = base64.b64encode(html)
url = 'data:text/html;base64,'+b64

console.show_activity('Starting server')

class RequestHandler (SimpleHTTPRequestHandler):
	def do_GET(self):
		self.send_response(303)
		self.send_header(unicode('Location'), unicode(url))
		self.end_headers()
		self.wfile.write('')
serv = BaseHTTPServer.HTTPServer(('', 0), RequestHandler)
port = serv.server_address[1]

console.show_activity('Opening')

Timer(1.5, webbrowser.open, ("safari-http://localhost:%d"%port,)).start()

serv.handle_request()
