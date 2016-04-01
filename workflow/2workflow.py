# https://forum.omz-software.com/topic/1918/using-workflow-app-with-pythonista/10

# coding: utf-8

from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer
import webbrowser

stopping = False

class StoppableHTTPServer (BaseHTTPServer.HTTPServer):
    def serve_forever(self, poll_interval=0.5):
        global stopping
        while not stopping:
            self._handle_request_noblock()
            
class RequestHandler (SimpleHTTPRequestHandler):
    def do_GET(self):
        global stopping
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write('hello')
        stopping = True
        
serv = StoppableHTTPServer(('', 25565), RequestHandler)
port = serv.server_address[1]

webbrowser.open('workflow://')
# serv.serve_forever()