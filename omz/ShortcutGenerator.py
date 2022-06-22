# https://gist.github.com/omz/7870550

# This script adds a "Webclip" shortcut to your homescreen.
# The shortcut can be used to open a web page in full-screen mode,
# or to launch a custom URL (e.g. a third-party app).
# You'll be asked for a title, a URL, and an icon (from your camera roll)

import console
try:
	import BaseHTTPServer
except:
	console.alert('This must be run in 2.7', 'Hold the run script button, then tap "Run with Python 2.7"')
	exit()
import plistlib
import webbrowser
import uuid
from io import BytesIO
import Image
import photos
import notification
import console
import PIL
import photos
from time import sleep
from objc_util import *
from ctypes import *

libobjc = CDLL('/usr/lib/libobjc.dylib')
LSAppilcationWorkspace = ObjCClass('LSApplicationWorkspace')
workspace = LSAppilcationWorkspace.defaultWorkspace()

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
	webbrowser.open('safari-http://localhost:' + str(sa[1]))
	httpd.handle_request()
	notification.schedule('Tap "Allow"')
	notification.schedule('Then, tap this notification to continue', 5, action_url = 'pythonista://')
	sleep(1.5)
	while console.is_in_background():
		None
	workspace.openApplicationWithBundleID("com.apple.Preferences")
	notification.remove_all_delivered()
	notification.schedule('Above "Aeroplane Mode" is a button showing "Profile Downloaded". Tap it, then tap "install"', 1)

def main():
	console.alert('Shortcut Generator', 'This script adds a "Webclip" shortcut to your homescreen. The shortcut can be used to open a web page in full-screen mode, or to launch a custom URL (e.g. a third-party app). You will be asked for a title, a URL, and an icon (from your camera roll).', 'Continue')
	name = console.input_alert('Shortcut Title', 'Please enter a short title for the homescreen icon.', '', 'Continue')
	if not name:
		return
	url = console.input_alert('Shortcut URL', 'Please enter the full URL that the shortcut should launch.', '', 'Continue')
	if not url:
		return
	asset = photos.pick_asset()
	if not asset:
		return
	
	description = name + ' icon'
	iconlabel = name
	img = asset.get_image()
	img.save('image.PNG')
	icon = PIL.Image.open('image.PNG')
	data_buffer = BytesIO()
	icon.save(data_buffer, 'PNG')
	icon_data = data_buffer.getvalue()
	unique_id = uuid.uuid4().urn[9:].upper()
	config = {'PayloadContent': [{'FullScreen': True,
		'Icon': plistlib.Data(icon_data),
		'IsRemovable': False,
		'Label': iconlabel,
		'PayloadIdentifier': 'com.omz-software.shortcut.' + unique_id,
		'PayloadOrganization': 'omz software',
		'PayloadType': 'com.apple.webClip.managed', 
		'PayloadUUID': unique_id, 'PayloadVersion': 1,
		'Precomposed': True, 'URL': url}],
		'PayloadDescription': description, 
		'PayloadDisplayName': name, 
		'PayloadIdentifier': unique_id,
		'PayloadOrganization': 'omz software',
		'PayloadRemovalDisallowed': False, 'PayloadType': #DO NOT TOUCH
		'Configuration', 'PayloadUUID': unique_id, 'PayloadVersion': 1}
	run_server(config)

if __name__ ==  '__main__':
	main()
