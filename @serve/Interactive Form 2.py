# Interactive Form 2
#
# https://gist.github.com/webvex/ce21319cfe042b6013bc
#
# https://forum.omz-software.com/topic/503/interactive-form-example/19
#
# Requires FormElements.py module available at:
#   https://gist.github.com/9e2163e1041a3e17d210
#
# This is a simple application with an HTML form interface.
# Enter an address, city, or zip code and select options.
# Static map images are returned from the Google Maps API.

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from string import Template
from FormElements import *
import cgi
import webbrowser

#form element option lists
type_opt = ['roadmap', 'satellite', 'hybrid', 'terrain']
zoom_opt = range(10)
size_opt = [['small', '320x240'], ['large', '640x480']]
mark_opt = [['&nbsp;', 'on']]

#form template
HTML = Template('<html><head>' +
  '<style type="text/css">' +
  '  body {margin: 30px; font-family: sans-serif; background: #eee;}' +
  '  span {font-weight: bold; font-style: italic; padding-left: 1em}' +
  '  img {display: block; margin-left: auto; margin-right: auto; ' +
         'box-shadow: 5px 5px 10px 0 #666;}' +
  '</style>' +
  '</head><body>' +
  '<form action="/" method="POST" enctype="multipart/form-data">' +
  '  <span>Location: </span>' + create_textbox('center', 20) +
  '  <span>View: </span>' + create_select('type', type_opt) +
  '  <span>Zoom: </span>' + create_select('zoom', zoom_opt) +
  '  <span>Size: </span>' + create_radios('size', size_opt) +
  '  <span>Marker: </span>' + create_checkboxes('mark', mark_opt) +
  '  &nbsp; <input type="submit" value="Get Map" />' +
  '</form>' +
  '<br/>${map}' +
  '</body></html>')
  
class RequestHandler(BaseHTTPRequestHandler):
	
  def do_GET(self):  #load initial page
	  subs = {'center': '', 'size_640x480': 'checked',
	          'map': 'Enter an address, city, or zip code.'}
	  self.send_response(200)
	  self.send_header('Content-Type', 'text/html')
	  self.end_headers()
	  self.wfile.write(HTML.safe_substitute(subs))
		
  def do_POST(self):  #process form requests
	  #read form data into variables
	  form = cgi.FieldStorage(fp = self.rfile, headers = self.headers,
		                        environ = {'REQUEST_METHOD':'POST',
		                       'CONTENT_TYPE':self.headers['Content-Type']})
	  c = form.getfirst('center')
	  t = form.getfirst('type')
	  z = form.getfirst('zoom')
	  s = form.getfirst('size')
	  m = str(form.getfirst('mark'))
	  #maintain form state
	  subs = {'center': c}
	  subs['type_' + t] = 'selected'
	  subs['zoom_' + z] = 'selected'
	  subs['size_' + s] = 'checked'
	  subs['mark_' + m] = 'checked'
	  #build map url string
	  if m == 'on': m = 'size:small%7C' + c
	  subs['map'] = ('<img src="http://maps.googleapis.com/maps/api/' +
	                 'staticmap?center=' + c + '&maptype=' + t +
	                 '&zoom=1' + z + '&size=' + s +
	                 '&markers=' + m + '&sensor=false">')
	  #send response
	  self.send_response(200)
	  self.send_header('Content-Type', 'text/html')
	  self.end_headers()
	  self.wfile.write(HTML.safe_substitute(subs))   

if __name__ == '__main__':	#start server and open browser
  server = HTTPServer(('', 80), RequestHandler)
  webbrowser.open('http://localhost', stop_when_done = True)
  server.serve_forever()