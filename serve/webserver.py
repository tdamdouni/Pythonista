from __future__ import print_function
import SimpleHTTPServer
import SocketServer
from os import chdir

chdir('./output/')

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()

