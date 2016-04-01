# coding: utf-8
import SocketServer, os
from SimpleHTTPServer import SimpleHTTPRequestHandler
from WebBrowser import WebBrowser

class ViewHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass 

if __name__ == "__main__":
    os.chdir(os.path.expanduser('~/Documents/ckeditor/'))
    wb = WebBrowser()
    wb.server = SocketServer.TCPServer(("", 0), ViewHandler)
    wb.open('http://localhost:' + str(wb.server.server_address[1]) + '/samples/')
    wb.server.serve_forever()