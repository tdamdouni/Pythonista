#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/3794/open-gif-or-image-in-safari/6

from SimpleHTTPServer import SimpleHTTPRequestHandler
import os
import shutil
import tempfile
import shutil
import webbrowser
import urllib
import time
from objc_util import nsurl,UIApplication
from socket import gethostname

PORT = 8080

if __name__ == '__main__':
    doc_path = os.path.expanduser('~/Documents')
    os.chdir(doc_path)
    
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('', PORT), SimpleHTTPRequestHandler)
    app = UIApplication.sharedApplication()
    URL = 'http://%s.local:8080' % gethostname()+'/IMG_5126.JPG'
    app.openURL_(nsurl(URL))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        print('Server stopped')
