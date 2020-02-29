from __future__ import print_function
# https://gist.github.com/Anton-2/6590539

# coding: utf-8

import socket
import webbrowser
import datetime
import json
from collections import namedtuple


class GeoLocationError(Exception):

	def __init__(self, code, message):
		self.code = code
		self.message = message
		
	def __str__(self):
		return 'code={}, msg={}'.format(self.code, self.message)
		
LocationInfo = namedtuple('LocationInfo', 'longitude latitude accuracy altitude altitudeAccuracy heading speed timestamp')


html = """
<!DOCTYPE html>
<html>
<head>
<script>

    function returnToPythonista() {
        window.open('pythonista://', '_self', '');
        window.setTimeout(function () {
           window.close();
        },0);
    }

                var xhr = new XMLHttpRequest();
                xhr.addEventListener("loadend", function () {
        window.setTimeout(returnToPythonista,0);
    }, false);

    xhr.open('POST', '/', true);

    function sendPosition(position) {
                        xhr.send(JSON.stringify([false, position]));
    }

                function handleError(positionError) {
        xhr.send(JSON.stringify([true, positionError]));
    }

    options = %s;
    navigator.geolocation.getCurrentPosition(sendPosition, handleError, options);

</script>
</head>

<body>
<h1>Wait...</h1>
</body>

</html>
"""

def get_location(port=3050, enableHighAccuracy=False, timeout=5000, maximumAge=0):

	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind( ('127.0.0.1', port) )
	s.listen(1)
	
	
	def send(data):
		s2, addrinfo = s.accept()
		resp = s2.recv(2048)
		
		body_len = None
		for line in resp.splitlines():
			if line.startswith('Content-Length'):
				body_len = int(line.split(':')[1])
				
		if body_len is not None:
			body_start = resp.index('\r\n\r\n')+4
			buf = resp[body_start:]
			resp = buf + s2.recv(body_len-len(buf))
		else:
			resp = ''
			
			
		s2.send("\r\n".join(("HTTP/1.0 200 OK", "Content-Type: text/html", "Content-Length: {}".format(len(data)), "", data)))
		
		s2.close()
		
		return resp
		
	webbrowser.open('safari-http://localhost:{}/'.format(port))
	
	
	# Send html page on first connection
	options = dict(enableHighAccuracy=enableHighAccuracy, timeout=timeout, maximumAge=maximumAge)
	send(html % json.dumps(options))
	
	# Send empty page, we are only interested in POST data
	data = send("")
	
	s.close()
	
	error, info = json.loads(data)
	
	if error:
		raise GeoLocationError(**info)
		
	timestamp = datetime.datetime.fromtimestamp(info['timestamp']/1000.0)
	return LocationInfo(timestamp=timestamp, **info['coords'])
	
	
if __name__ == '__main__':

	try:
		loc = get_location(enableHighAccuracy=False)
		print('loc: ', loc)
	except GeoLocationError as error:
		print('failed: ', error.message)

