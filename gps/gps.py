# https://forum.omz-software.com/topic/249/gps-access-solved/9

# coding: utf-8


theURL = 'http://www.w3schools.com/html/tryit.asp?filename=tryhtml5_geolocation'
import webbrowser; webbrowser.open(theURL)


import requests; print(requests.get(theURL).text)



#<pre>

#getGPS using html5 and interactive form

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import cgi
import webbrowser

HTML = ('<!DOCTYPE html>' +
'<html>'+
'<body>'+
'<form id="frm" action="/" method="POST" enctype="multipart/form-data">'+
'<input type="text" name="lat" id="lat" value="" />'+
'<input type="text" name="lng" id="lng" value="" />'+
'</form>'+
'<script>'+
'var frm=document.getElementById("frm");'+
'var lat=document.getElementById("lat");'+
'var lng=document.getElementById("lng");'+
'navigator.geolocation.getCurrentPosition(showPosition);'+
'function showPosition(position)'+
'{'+
' lat.value=position.coords.latitude;'+
' lng.value=position.coords.longitude;'+
' frm.submit();'
'}'+
'</script>'+
'</body>'+
'</html>')

class RequestHandler(BaseHTTPRequestHandler):

def do_GET(self): #load initial page
self.send_response(200)
self.send_header('Content-Type', 'text/html')
self.end_headers()
self.wfile.write(HTML)

def do_POST(self): #process requests
#read form data
form = cgi.FieldStorage(fp = self.rfile, headers = self.headers,
environ = {'REQUEST_METHOD':'POST',
'CONTENT_TYPE':self.headers['Content-Type']})
#assign variables
lat = form.getfirst('lat')
lng = form.getfirst('lng')
print((lat,lng))

if name == 'main': #start server and open browser
server = HTTPServer(('', 80), RequestHandler)
webbrowser.open('http://localhost', stop_when_done = True)
server.serve_forever()
</pre>


#<pre>

#getGPS using html5 and interactive form

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import cgi
import webbrowser
import time

HTML = ("""<!DOCTYPE html>
<html>
<body>
<p id="demo">Click the button to get your coordinates:</p>
<form id="frm" action="/" method="POST" enctype="multipart/form-data">
<input type="text" name="lat" id="lat" value="" />
<input type="text" name="lng" id="lng" value="" />
</form>
<script>
var frm=document.getElementById("frm");
var lat=document.getElementById("lat");
var lng=document.getElementById("lng");

navigator.geolocation.getCurrentPosition(showPosition);

function showPosition(position)
{
lat.value=position.coords.latitude;
lng.value=position.coords.longitude;
window.setTimeout(submitPosition,2000)
}
function submitPosition()
{
frm.submit()
}
</script>
</body>
</html>""")

class RequestHandler(BaseHTTPRequestHandler):

def do_GET(self): #load initial page
self.send_response(200)
self.send_header('Content-Type', 'text/html')
self.end_headers()
self.wfile.write(HTML)

def do_POST(self): #process requests
#read form data
form = cgi.FieldStorage(fp = self.rfile, headers = self.headers,
environ = {'REQUEST_METHOD':'POST',
'CONTENT_TYPE':self.headers['Content-Type']})
#assign variables
lat = form.getfirst('lat')
lng = form.getfirst('lng')
print((lat,lng))
self.send_response(200)
self.send_header('Content-Type','text/html')
self.end_headers()
self.wfile.write(HTML)

if name == 'main': #start server and open browser
server = HTTPServer(('', 80), RequestHandler)
webbrowser.open('http://localhost', stop_when_done = True)
server.serve_forever()
</pre>


from gpsForPythonista import getGPS;     print(getGPS())      # or...
from gpsForPythonista import getLatLong; print(getLatLong())  # or...
from gpsForPythonista import getGPS;     print(getGPS().altitude)

