from __future__ import print_function
import SimpleHTTPServer
import SocketServer
import webbrowser
import socket

ip_addr = socket.gethostbyaddr(socket.getfqdn())[2]

port = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", port), Handler)

print("Serving on IP address: ", ip_addr)
print("Serving on port: ", port)
httpd.serve_forever()
