from __future__ import print_function
import uuid, BaseHTTPServer, select, types, webbrowser, editor, os, urllib
from SimpleHTTPServer import SimpleHTTPRequestHandler
try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO
	
global mobile_config_str
mobile_config_str = ''

global base_mobileconfig
base_mobileconfig = ''

global keep_running
keep_running = True

# The Icon key contains a base64 encoded green version of the Pythonista low-res
# icon (for shortness)

base_mobileconfig = """
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>PayloadContent</key><array><dict>
<key>FullScreen</key><true/>
<key>Icon</key><data>
iVBORw0KGgoAAAANSUhEUgAAADkAAAA5CAMAAAC7xnO3AAACHFBMVEWl0KCp0qREej1DeDxIgkFHgUBKhkOYyZJMiUS32bPN5cpNik
Wz167C37612LHO5cuhzpy22bK93LlQkUjE4MGezJjF4cKz16/B3r2v1arD37+s06eQxYpOjUZRkkmy1q2RxYvR586ZyZO627ZRk0mP
xIiLwoRXnU6gzZpUmUxTlkuSxoyUx46WyJDf7t2GwH9vtGdrsWJnr15+u3bg7t7m8uVytWpztmt6uXJpsGDj8OF8unR2t26BvXposF
/c7Nro8+fs9evh7994uHBkrltgrFdwtGjw9+9ssmPk8OKCvnttsmRus2bV6dNeq1Xn8uZdqlR0tmzz+PKHwIDq9Ok9bjfU6NH2+vZ3
uG/S58+Fv377/fvb7Nnv9u5jrVp7unNlrlz6/Pr9/v07ajXV6dL2+vXl8eP3+/fu9u1hrFjX6tV/vHc7azXy+PHY6taDvnw+cDh/vH
g/cjnZ69f///8/czmJwYI5ZzPd7dv0+fOKwYPr9Oo5ZjP+/v46aDQ9bzdcp1P5/PldqVTI4sVBdjtcplNEez1CdztJhUJbpVLG4cM8
bDY3ZDJGfz82YzFYn0/K48dGfj+r06ZPjkdZoVC52rWkz5/J48ZYnk+Ow4e/3buw1auNw4ZIg0G+3bpao1FNi0XM5Mmdy5eo0aPQ5s
2aypRFfD6t1Kg0Xy9AdDqcy5ZaolGgzZu727dSlUpTl0un0aJKh0NPj0dVmk295pW9AAAJrUlEQVR4XiRUA9vlzBLML4pt+9i2/dpe
ez/buNYfvJ3dyjyTru6qnjknySDeB+RPT738apWHC5CE3ipBEgD7SCGEzGn+owUZASojI9Dm2ro532/CrM2byX1/Pl/P5/v7WnO91r
T5Wpvvz7V9NJiCHoDcAjyzqZ00myeopmknNErTJ0BpDTI0jaKo1tRoDYX4BAUVTQdeYkIuL/stE6UDUxQDMaCDgBZN1KRRMQhEVASf
iNImipomHaAmZEFnBkb/8hKcefAw4zEzFpkxQByPg48XEzAAoIHIiAFomADKojhmmDw4+72inskwReYD9GKxmMnojK4zGSYZwD/mgU
EFEjoETLHXR3orXdenIJgSpT9fXgxeLK9Lx4Pt8ni5XG6X14Pri+WytCwdl14MShcviKlxPjWKRnHVQyZTb2VMp63Pt69sBTsqbLCz
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
hLfvZ+RfO8pfTF65YHcAAAAASUVORK5CYII=
</data>
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
<key>PayloadOrganization</key><string>with help from pudquick</string>
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
		if mobile_config_str:
			mobileconfig = mobile_config_str
		else:
			mobileconfig = ' '
		self.send_response(200)
		self.send_header("Last-Modified", self.date_time_string())
		self.send_header("Content-type", "application/x-apple-aspen-config")
		self.send_header("Content-Length", len(mobileconfig))
		self.end_headers()
		f = StringIO()
		f.write(mobileconfig)
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
		# More limited form of serve forever - shutdown after mobileconfig download
		# Works in a single thread
		global keep_running
		while keep_running:
			self._handle_request_noblock()
			
def serve_it_up(port):
	global mobile_config_str
	global base_mobileconfig
	ip = '127.0.0.1'
	
	path = editor.get_path()
	name, ext = os.path.splitext(os.path.basename(path))
	
	icon_label = name
	UUID1 = str(uuid.uuid4()).upper()
	script_name = urllib.quote(name)
	arg_str = ''
	payload_name = 'Pythonista - %s' % icon_label
	UUID2 = str(uuid.uuid4()).upper()
	mobile_config_str = base_mobileconfig % (icon_label, UUID1, UUID1, script_name, arg_str, payload_name, UUID2, UUID2)
	my_httpd = NicerHTTPServer((ip, port), MobileConfigHTTPRequestHandler)
	print("Serving HTTP on %s:%s ..." % (ip,port))
	my_httpd.serve_forever()
	print("\n*** Webclip installed! ***")
	
port = 8000
webbrowser.open('safari-http://127.0.0.1:%s/webclip.mobileconfig' % port)
serve_it_up(port)

