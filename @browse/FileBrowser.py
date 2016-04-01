import SimpleHTTPServer
import SocketServer
import webbrowser
import os
os.chdir('/')
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", 0), Handler)
port = httpd.server_address[1]
webbrowser.open('http://localhost:' + str(port), stop_when_done=True)
httpd.serve_forever()
