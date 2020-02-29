from __future__ import print_function
import uuid, BaseHTTPServer, select, types, clipboard, console, photos, PIL, base64, urllib, webbrowser
from SimpleHTTPServer import SimpleHTTPRequestHandler
try: from cStringIO import StringIO
except ImportError: from StringIO import StringIO

keep_running = True
base_mobileconfig = """
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>PayloadContent</key><array><dict>
<key>FullScreen</key><true/>
<key>Icon</key><data>%s</data>
<key>IsRemovable</key><true/>
<key>Label</key><string>%s</string>
<key>PayloadDescription</key><string>Configures Web Clip</string>
<key>PayloadDisplayName</key><string>Web Clip (Pythonista)</string>
<key>PayloadIdentifier</key><string>com.pudquick.profile.%s</string>
<key>PayloadOrganization</key><string>Pythonista</string>
<key>PayloadType</key><string>com.apple.webClip.managed</string>
<key>PayloadUUID</key><string>%s</string>
<key>PayloadVersion</key><integer>1</integer>
<key>Precomposed</key><true/>
<key>URL</key><string>pythonista://%s?action=run&amp;args=%s</string>
</dict></array>
<key>PayloadDescription</key><string>Pythonista Web Clip</string>
<key>PayloadDisplayName</key><string>%s</string>
<key>PayloadIdentifier</key><string>com.pudquick.profile.%s</string>
<key>PayloadOrganization</key><string>%s</string>
<key>PayloadRemovalDisallowed</key><false/>
<key>PayloadType</key><string>Configuration</string>
<key>PayloadUUID</key><string>%s</string>
<key>PayloadVersion</key><integer>1</integer>
</dict></plist>
"""

class MobileConfigHTTPRequestHandler(SimpleHTTPRequestHandler):
	def offer_generic(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.send_header("Last-Modified", self.date_time_string())
		self.end_headers()
		
		f = StringIO()
		f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
		f.write('<html><body><a href="\webclip.mobileconfig">Something odd happened, click here instead</a></body></html>\n')
		f.seek(0)
		self.copyfile(f, self.wfile)
		f.close()
		
	def offer_mobileconfig(self):
		global mobile_config_str
		
		self.send_response(200)
		self.send_header("Last-Modified", self.date_time_string())
		self.send_header("Content-type", "application/x-apple-aspen-config")
		self.send_header("Content-Length", len(mobile_config_str))
		self.end_headers()
		
		f = StringIO()
		f.write(mobile_config_str)
		f.seek(0)
		self.copyfile(f, self.wfile)
		f.close()
		
		global keep_running
		keep_running = False
		
	def do_GET(self):
		if (self.path.lower().endswith('.mobileconfig')):
			return self.offer_mobileconfig()
		return self.offer_generic()

class NicerHTTPServer(BaseHTTPServer.HTTPServer):
	def serve_forever(self, poll_interval=0.5):
		global keep_running
		while keep_running:
			self._handle_request_noblock()

ip = '127.0.0.1'
port = 8000

icon_label = console.input_alert('Homescreen name')
script_name = console.input_alert('Script path')
arg_str = console.input_alert('Script arguments')
payload_name = 'Pythonista Script'

console.alert('Please select an icon', '', 'Ok')
png_data = StringIO()
photos.pick_image().save(png_data, format='PNG')
png_str = base64.b64encode(png_data.getvalue())
png_data.close()

UUID1 = uuid.uuid4()
UUID2 = uuid.uuid4()

mobile_config_str = base_mobileconfig % (png_str, icon_label, UUID1, UUID1, urllib.quote(script_name), arg_str, payload_name, UUID2, script_name, UUID2)

clipboard.set('http://%s:%s/webclip.mobileconfig' % (ip, port))

console.clear()
console.set_font('Futura', 16)
console.set_color(0.2, 0.2, 1)
print("Safari will open automatically. Alternatively, you can open Safari manually and paste in the URL on your clipboard.\n")
console.set_font()
console.set_color()

my_httpd = NicerHTTPServer((ip, port), MobileConfigHTTPRequestHandler)
print("Serving HTTP on %s:%s ..." % (ip, port))

webbrowser.open('safari-http://%s:%s/webclip.mobileconfig' % (ip, port))
my_httpd.serve_forever()

print("\n*** Webclip installed! ***")

