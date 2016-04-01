# coding: utf-8

# https://gist.github.com/webvex/104bb2a5c79cda02cdd2

# https://forum.omz-software.com/topic/503/interactive-form-example

# Interactive Form
#
# This is a simple application with an HTML form interface.
# Enter an address, city, or zip code and select options.
# Static map images are returned from the Google Maps API.

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from string import Template
import cgi
import webbrowser

HTML = Template('<html><head>' +
  '<style type="text/css">' +
  ' body {margin: 30px; font-family: sans-serif; background: #ddd;}' +
  ' span {font-weight: bold; font-style: italic; padding-left: 1em}' +
  ' img {display: block; margin-left: auto; margin-right: auto; ' +
        'box-shadow: 5px 5px 10px 0 #666;}' +
  '</style></head><body>' +
  '<form action="/" method="POST" enctype="multipart/form-data">' +
  ' <span>Location:</span>' +
  ' <input type="text" name="center" value="${center}" />' +
  ' <span>View:</span>' +
  ' <select name="type" onchange="form.submit()">' +
  ' <option ${t_roadmap}>roadmap<option ${t_satellite}>satellite' +
  ' <option ${t_hybrid}>hybrid<option ${t_terrain}>terrain</select>' +
  ' <span>Zoom:</span>' +
  ' <select name="zoom" onchange="form.submit()">' +
  ' <option ${z_0}>0<option ${z_1}>1<option ${z_2}>2<option ${z_3}>3' +
  ' <option ${z_4}>4<option ${z_5}>5<option ${z_6}>6<option ${z_7}>7' +
  ' <option ${z_8}>8<option ${z_9}>9</select>' +
  ' <span>Size:</span>' +
  ' <input type="radio" name="size" value="320x240" ' +
  ' onclick="form.submit()" ${s_320x240} />Small ' +
  ' <input type="radio" name="size" value="640x480" ' +
  ' onclick="form.submit()" ${s_640x480} />Large' +
  ' <span>Marker:</span>' +
  ' <input type="checkbox" name="mark" value="on" ' +
  ' onclick="form.submit()" ${m_on} /> '
  ' &nbsp; <input type="submit" value="Get Map" />' +
  '</form>' +
  '<br/> ${map}' +
  '</body></html>')
  
class RequestHandler(BaseHTTPRequestHandler):
	
  def do_GET(self):  #load initial page
	  subs = {'center': '', 's_640x480': 'checked',
	          'map': 'Enter an address, city, or zip code.'}
	  self.send_response(200)
	  self.send_header('Content-Type', 'text/html')
	  self.end_headers()
	  self.wfile.write(HTML.safe_substitute(subs))
		
  def do_POST(self):  #process requests
    #read form data
	  form = cgi.FieldStorage(fp = self.rfile, headers = self.headers,
		                        environ = {'REQUEST_METHOD':'POST',
		                       'CONTENT_TYPE':self.headers['Content-Type']})
	  #assign variables
	  c = form.getfirst('center')
	  t = form.getfirst('type')
	  z = form.getfirst('zoom')
	  s = form.getfirst('size')
	  m = str(form.getfirst('mark'))
	  #maintain form state
	  subs = {'center': c}
	  subs['t_' + t] = 'selected'
	  subs['z_' + z] = 'selected'
	  subs['s_' + s] = 'checked'
	  subs['m_' + m] = 'checked'
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