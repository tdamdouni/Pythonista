#coding: utf-8
import urllib
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import webbrowser
import os
from threading import Timer
import base64
from ui import Image
import console
import sys
import io

sys.stderr = io.StringIO()

console.show_activity('Creating images…')


imagefilenames = [os.path.splitext(i)[0] for i in open(os.path.expanduser('~/Pythonista.app/Typicons-M.txt')).readlines()]

imagenames = [i.replace('Typicons96_', '') for i in imagefilenames]

images = {n: Image.named(imagefilenames[i]) for (i, n) in enumerate(imagenames)}

imageurls = {k:'data:image/png;base64,'+base64.b64encode(images[k].to_png()) for k in images}

choosecolorpath = os.path.dirname(sys.argv[0].split('/Documents/',1)[1]) + '/choosecolor.py'

tagtemplate = '<a href="pythonista://' +choosecolorpath+ '?action=run&argv=%s"><img src="%s"></a>'

imagetags = [tagtemplate%(k,imageurls[k]) for k in imagenames]

imagesstring = ''.join(imagetags)

html = '''
<!DOCTYPE html>
<html>
<head>
<style type="text/css">
body {
	background:#292929;
	text-align:center;
	line-height:0;
	margin:0;
}
img {
	width:48px;
	height:48px;
	padding:6px;
	margin:8px;
	background-color:#707070;
	background: linear-gradient(#707070, #5a5a5a);
	border-radius:14px;
	box-shadow:0 2px 4px rgba(0,0,0,0.5);
}
h1 {
	font-family:"Avenir Next";
	color: white;
	padding: 10px;
	text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}
</style>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
</head>
<body>
<h1>Choose an Icon</h1>
%s
</body>
</html>
''' % imagesstring

class RequestHandler (SimpleHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(html)
	def log_message(self, format, *args):
		pass
		
serv = BaseHTTPServer.HTTPServer(('', 0), RequestHandler)
port = serv.server_port

Timer(1, webbrowser.open, ('http://localhost:%d'%port,)).start()

console.show_activity('Starting server…')
serv.handle_request()
console.hide_activity()
