# This script adds a "Webclip" shortcut to your homescreen.
# The shortcut can be used to open a web page in full-screen mode,
# or to launch a custom URL (e.g. a third-party app).
# You'll be asked for a title, a URL, and an icon (from your camera roll)

import plistlib
import BaseHTTPServer
import webbrowser
import uuid
from io import BytesIO
import Image
import photos
import notification
import console

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
	notification.schedule('Tap "Install" to add the shortcut to your homescreen.', 1.0)

def main():
	console.alert('Shortcut Generator', 'This script adds a "Webclip" shortcut to your homescreen. The shortcut can be used to open a web page in full-screen mode, or to launch a custom URL (e.g. a third-party app). You\'ll be asked for a title, a URL, and an icon (from your camera roll).', 'Continue')
	label = console.input_alert('Shortcut Title', 'Please enter a short title for the homescreen icon.', '', 'Continue')
	if not label:
		return
	url = console.input_alert('Shortcut URL', 'Please enter the full URL that the shortcut should launch.', '', 'Continue')
	if not url:
		return
	icon = photos.pick_image()
	if not icon:
		return
	console.show_activity('Preparing Configuration profile...')
	data_buffer = BytesIO()
	icon.save(data_buffer, 'PNG')
	icon_data = data_buffer.getvalue()
	unique_id = uuid.uuid4().urn[9:].upper()
	config = {'PayloadContent': [{'FullScreen': True,
            'Icon': plistlib.Data(icon_data), 'IsRemovable': True,
            'Label': label, 'PayloadDescription': 'Configures Web Clip', 
            'PayloadDisplayName': label,
            'PayloadIdentifier': 'com.omz-software.shortcut.' + unique_id, 
            'PayloadOrganization': 'omz:software', 
            'PayloadType': 'com.apple.webClip.managed',
            'PayloadUUID': unique_id, 'PayloadVersion': 1,
            'Precomposed': True, 'URL': url}], 
            'PayloadDescription': label,
            'PayloadDisplayName': label + ' (Shortcut)', 
            'PayloadIdentifier': 'com.omz-software.shortcut.' + unique_id,
            'PayloadOrganization': 'omz:software', 
            'PayloadRemovalDisallowed': False, 'PayloadType': 
            'Configuration', 'PayloadUUID': unique_id, 'PayloadVersion': 1}
	console.hide_activity()
	run_server(config)

if __name__ ==  '__main__':
	main()

