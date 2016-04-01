# http://omz-forums.appspot.com/pythonista/post/5842985077964800

# FontInstaller (by @olemoritz)

# This script installs a custom TTF font on iOS (system-wide).
# It can be used in one of two ways:

# 1. Simply run it in Pythonista, you'll be prompted for the URL of the font 
#    you'd like to install (if there's a URL in the clipboard, it'll be used by default)

# 2. Use it as an 'Open in...' handler, i.e. select this file in Pythonista's 'Open in...
#    menu' setting. This way, you can simply download a ttf file in Safari and open it in
#    Pythonista. The script will then automatically install the downloaded font.

# The script is inspired by the AnyFont app (https://itunes.apple.com/us/app/anyfont/id821560738)
# and the iOS integration of MyFonts (http://meta.myfonts.com/post/80802984786/install-fonts-from-myfonts-on-ios-7-devices)

import plistlib
import BaseHTTPServer
import webbrowser
import uuid
import urllib
import sys
import console
import clipboard
import os

# Request handler for serving the config profile:
class ConfigProfileHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    config = None
    def do_GET(s):
        s.send_response(200)
        s.send_header('Content-Type', 'application/x-apple-aspen-config')
        s.end_headers()
        plist_string = plistlib.writePlistToString(ConfigProfileHandler.config)
        s.wfile.write(plist_string)
    def log_message(self, format, *args):

         pass

def run_server(config):
    ConfigProfileHandler.config = config
    server_address = ('', 0)
    httpd = BaseHTTPServer.HTTPServer(server_address, ConfigProfileHandler)
    sa = httpd.socket.getsockname()
    # Point Safari to the local http server:
    webbrowser.open('safari-http://localhost:' + str(sa[1]))
    # Handle a single request, then stop the server:
    httpd.handle_request()

def main():
    with open('Ubuntu-R.ttf', 'r') as f:
            ur = f.read()
    with open('Ubuntu-RI.ttf', 'r') as f:
            uri = f.read()
    with open('Ubuntu-B.ttf', 'r') as f:
            ub = f.read()
    with open('Ubuntu-BI.ttf', 'r') as f:
            ubi = f.read()
    with open('Ubuntu-C.ttf', 'r') as f:
            uc = f.read()
    with open('Ubuntu-L.ttf', 'r') as f:
            ul = f.read()
    with open('Ubuntu-LI.ttf', 'r') as f:
            uli = f.read()
    with open('Ubuntu-M.ttf', 'r') as f:
            um = f.read()
    with open('Ubuntu-MI.ttf', 'r') as f:
            umi = f.read()

    # Create the configuration profile:
    unique_id = uuid.uuid4().urn[9:].upper()
    config = {'PayloadContent': [{
              'Font': plistlib.Data(ur),
              'PayloadIdentifier': 'org.ubuntu.font.' + unique_id, 
              'PayloadOrganization': 'Ubuntu',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': unique_id, 'PayloadVersion': 1},
              {'Font': plistlib.Data(uri),
               'PayloadIdentifier': 'org.ubuntu.font.' + '342', 
              'PayloadOrganization': 'Ubuntu',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '74654', 'PayloadVersion': 1},
              {'Font': plistlib.Data(ub),
               'PayloadIdentifier': 'org.ubuntu.font.' + '995', 
              'PayloadOrganization': 'Ubuntu',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '5445', 'PayloadVersion': 1},
              {'Font': plistlib.Data(ubi),
               'PayloadIdentifier': 'org.ubuntu.font.' + '55664', 
              'PayloadOrganization': 'Ubuntu',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '46423', 'PayloadVersion': 1},
              {'Font': plistlib.Data(uc),
               'PayloadIdentifier': 'org.ubuntu.font.' + '56455', 
              'PayloadOrganization': 'Ubuntu',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '4543', 'PayloadVersion': 1},
              {'Font': plistlib.Data(ul),
               'PayloadIdentifier': 'org.ubuntu.font.' + unique_id, 
              'PayloadOrganization': 'Ubuntu',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '13', 'PayloadVersion': 1},
              {'Font': plistlib.Data(uli),
               'PayloadIdentifier': 'org.ubuntu.font.' + '5334', 
              'PayloadOrganization': 'Ubuntu',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '123', 'PayloadVersion': 1},
              {'Font': plistlib.Data(um),
               'PayloadIdentifier': 'org.ubuntu.font.' + '5445', 
              'PayloadOrganization': 'Ubuntu',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '57888', 'PayloadVersion': 1},
              {'Font': plistlib.Data(umi),
               'PayloadIdentifier': 'org.ubuntu.font.' + '54444', 
              'PayloadOrganization': 'Ubuntu',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '46544', 'PayloadVersion': 1},
              ], 
            'PayloadDescription': 'Ubuntu',
            'PayloadDisplayName': 'Ubuntu',
            'PayloadIdentifier': 'org.ubuntu.font.' + unique_id,
            'PayloadOrganization': 'Ubuntu', 
            'PayloadRemovalDisallowed': False, 
            'PayloadType': 'Configuration',
            'PayloadUUID': unique_id,
            'PayloadVersion': 1}
    run_server(config)

if __name__ ==  '__main__':
    main()

# def font_dict(filename, payload_id=None, payload_uuid=None):
#    payload_id = payload_id or uuid.uuid4().urn[9:].upper()
#    payload_uuid = payload_uuid or payload_id
#    with open(filename) as in_file:
#        font_data = in_file.read()
#    return { 'Font': plistlib.Data(font_data),
#              'PayloadIdentifier': 'org.scj643.font.{}'.format(payload_id)
#              'PayloadOrganization': 'scj643',
#              'PayloadType': 'com.apple.font',
#              'PayloadUUID': payload_uuid,
#              'PayloadVersion': 1 }

#     config = {'PayloadContent': [font_dict('Ubuntu-{}.ttf'.format(x))
#                                 for x in 'R RI B BI C L LI M MI'.split()]
#               ...
