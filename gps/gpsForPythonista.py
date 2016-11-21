# The GPS issue was fixed quite elegantly with the location module
# added in Pythonista v1.4.  The code below is not longer required.

# gpsForPythonista using BaseHTTPServer and XMLHttpRequest
# Source at https://gist.github.com/cclauss/6578926
# Thanks to 'Hvmhvm' of Pythonisa fourm for working code
# Thanks to 'Anton2' of Pythonisa fourm for XMLHttpRequest
# http://omz-software.com/pythonista/forums/discussion/92/gps-access-solved

# usage: from gpsForPythonista import getGPS; print(getGPS())
#    or  from gpsForPythonista import getLatLong; print(getLatLong())
#    or  from gpsForPythonista import getGPS; print(getGPS().altitude)

import BaseHTTPServer, cgi, webbrowser
from collections import namedtuple

GPSfields  = ('latitude', 'longitude', 'altitude', 'accuracy',
          'altitudeAccuracy', 'heading', 'speed', 'timestamp')
GPSvalues  = namedtuple('GPSvalues', GPSfields)
gGPSvalues = None  # Global variable that will hold GPS info

HTML = """<!DOCTYPE html>
<html>
  <body>
    <div style="text-align:center;">
      <H1>Gathering GPS data...  Tap the Done button to see the results...</H1>
      <H2>Please ensure that Localization Services are enabled for Pythonista:</H2>
      <H3>Settings app --> Privacy --> Localization Services --> Pythonista (ON)</H3>
    </div>
    <script>
      function returnToPythonista()
      {
        window.open('pythonista://', '_self', '');
        window.setTimeout(function () {
           window.close();
        }, 100);
      }

      function sendPosition(position)
      {
        var xhr = new XMLHttpRequest();

        xhr.addEventListener("loadend", function () {
            window.setTimeout(returnToPythonista, 100);
        }, false);

        xhr.open('POST', '', true);
        xhr.send(position.coords.latitude + '&'
               + position.coords.longitude + '&'
               + position.coords.altitude + '&'
               + position.coords.accuracy + '&'
               + position.coords.altitudeAccuracy + '&'
               + position.coords.heading + '&'
               + position.coords.speed + '&'
               + new Date(position.timestamp).toLocaleString())
      }

      navigator.geolocation.getCurrentPosition(sendPosition);
    </script>
  </body>
</html>"""

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def sendHeaders(self):
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		
	def do_GET(self):   # load initial page
		self.sendHeaders()
		self.wfile.write(HTML)
		
	def do_POST(self):  # process request
		contentLength = int(self.headers.getheader('content-length'))
		postBody = self.rfile.read(contentLength)
		global gGPSvalues
		gGPSvalues = GPSvalues(*postBody.split('&'))
		
def getGPS():
	global gGPSvalues
	gGPSvalues = None
	httpd = BaseHTTPServer.HTTPServer(('', 80), RequestHandler)
	webbrowser.open('safari-http://localhost')  # try both http:// and safari-http://
	while not gGPSvalues:
		httpd.handle_request()
	return gGPSvalues
	
def getLatLong():
	GPSvalues = getGPS()
	return (float(GPSvalues.latitude),
	float(GPSvalues.longitude))
	
if __name__ == '__main__':
	#print(getLatLong())  # safari-http:// stops the script here
	print(getGPS())
	print(getGPS().altitude)

