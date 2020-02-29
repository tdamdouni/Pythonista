from __future__ import print_function
import socket
import webbrowser
import re
 
html = """
<!DOCTYPE html>
<html>
<head>
<script>
 
    function returnToPythonista() {
        window.open('pythonista://', '_self', '');
        window.setTimeout(function () {
           window.close();  
        },100);
    }
 
    function sendPosition(position) {
        var xhr = new XMLHttpRequest();
 
        xhr.addEventListener("loadend", function () {
            window.setTimeout(returnToPythonista,100);
        }, false);
 
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
 
        xhr.open('HEAD', '/?lat=' + lat + '&lng=' + lng, true);
        xhr.send("");
    }
 
    navigator.geolocation.getCurrentPosition(sendPosition);
 
</script>
</head>
 
<body>
<h1>Wait...</h1>
</body>
 
</html>
"""
 
def getLocation(port=3050):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind( ('127.0.0.1', port) )
    s.listen(1)
 
    webbrowser.open('safari-http://localhost:{}/'.format(port))
 
    def send(data):
        s2, addrinfo = s.accept()
        resp = s2.recv(4096)
        s2.send("\n".join(("HTTP/1.0 200 OK", "Content-Type: text/html", "Content-Length: {}".format(len(data)), "", data)))
        s2.close()
        
        return resp
 
    # Send html page on first connection
    send(html)
 
    # Send empty page
    data = send("")
    
    s.close()
 
    result = re.search(r'lat=([\d.]*)&lng=([\d.]*)', data)
    if result:
        return [float(n) for n in result.groups()]
 
    return None, None
 
 
if __name__ == '__main__':
    lat, lng = getLocation()
    print(lat, lng)
