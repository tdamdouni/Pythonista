# https://gist.github.com/webvex/5ae84d7508619befd2c2

# This is an old version. Please use the newer version at:
#   https://gist.github.com/104bb2a5c79cda02cdd2

# Interactive Form
#
# This is a simple application with an HTML form interface.
# Enter a city, zip code or address and select options.
# Static map images are returned from the Google Maps API.

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import cgi
import webbrowser

TEMPLATE = ('<!DOCTYPE html><html><head></head>' +
  '<body style="margin:20px; font-family:sans-serif; background:#ddd">' +
  '<h2>Interactive Form</h2>' + 
  '<form action="/" method="POST" enctype="multipart/form-data">' +
  '<strong> Location: </strong>' +
  '<input type="text" name="center" value="{{CENTER}}"></input>' +
  '<strong> &nbsp; &nbsp; Type: </strong>' +
  '<select name="type" style="width:90px" onchange="form.submit()">' +
  '<option>roadmap<option>satellite<option>terrain<option>hybrid</select>' +
  '<strong> &nbsp; &nbsp; Zoom: </strong>' +
  '<select name="zoom" style="width:50px" onchange="form.submit()">' +
  '<option>0<option>1<option>2<option>3<option>4' +
  '<option>5<option>6<option>7<option>8<option>9</select>' +
  '<strong> &nbsp; &nbsp; Size: </strong>' +
  '<input type="radio" name="size" value="320x240" ' +
  'onclick="form.submit()">Small ' +
  '<input type="radio" name="size" value="640x480" ' +
  'onclick="form.submit()">Large ' +
  '&nbsp; &nbsp; <input type="submit" value="Get Map">' +
  '</form><br/><br/>{{MAP}}</body></html>')
  
class RequestHandler(BaseHTTPRequestHandler):
	
  def do_GET(self):  #load initial page
    html = TEMPLATE.replace('{{CENTER}}', '')
    html = html.replace('>Small', ' checked>Small')
    html = html.replace('{{MAP}}', '')
    self.send_response(200)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    self.wfile.write(html)
		
  def do_POST(self):  #process requests
    form = cgi.FieldStorage(fp = self.rfile, headers = self.headers,
	                   environ = {'REQUEST_METHOD':'POST', 
	                  'CONTENT_TYPE':self.headers['Content-Type']})
    c = form.getvalue('center')
    t = form.getvalue('type')
    z = form.getvalue('zoom')
    s = form.getvalue('size')
    m = ('<img src="http://maps.googleapis.com/maps/api/staticmap?' +
         'center=' + c + '&maptype=' + t + '&zoom=1' + z + 
         '&size=' + s + '&markers=' + c +'&sensor=false">')
    html = TEMPLATE.replace('{{CENTER}}', c)
    html = html.replace('>' + t, ' selected>' + t)
    html = html.replace('>' + z, ' selected>' + z)
    if s == '320x240':
      html = html.replace('>Small', ' checked>Small')
    else:
      html = html.replace('>Large', ' checked>Large')
    html = html.replace('{{MAP}}', m)
    self.send_response(200)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    self.wfile.write(html)

if __name__ == '__main__':  #start server and open browser
  server = HTTPServer(('', 80), RequestHandler)
  webbrowser.open('http://localhost', stop_when_done = True)
  server.serve_forever()
