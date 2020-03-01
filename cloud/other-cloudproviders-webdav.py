# coding: utf-8

# https://forum.omz-software.com/topic/2917/other-cloudproviders-webdav

import requests, os, socket, random, string, shutil, urllib
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
DAVurl = None
DAVport = None

class __CloudProvider(object):
	"""implementation using WebDAV server modified to mimic secret Gist"""
	def putFileToURL(self, f):
		s = requests.session()
		s.headers = {'User-Agent':'__CloudProvider'}
		response = s.request('PUT', 'http://' + DAVurl + ':' + str(DAVport), data = f)
		return response.headers['URL']
		
		def getFileFromURL(self, sURL):
			return urllib.urlopen('http://' + DAVurl + ':' + str(DAVport) + '/' + sURL)
			
			
class DAVRequestHandler(BaseHTTPRequestHandler):
	"""mimic secret Gist"""
	def do_GET(self, oh = False):
		sF = os.path.expanduser('~/Documents/cloud-files/' + self.path.split('/')[1])
		if len(self.path.split('/')) > 2 or '.' in self.path or not os.path.isfile(sF):
			self.send_error(404, 'Object not found')
			return
		iS = os.stat(sF).st_size
		self.send_response(200, 'OK')
		self.send_header("Content-length", iS)
		self.end_headers()
		if iS > 0:
			with open(sF, 'rb') as f:
				shutil.copyfileobj(f, self.wfile, length = 512 * 1024)
				
	def do_PUT(self):
		if self.headers['User-Agent'] != '__CloudProvider':
			self.send_response(403, 'Forbidden')
			self.send_header('Content-length', '0')
			self.end_headers()
			return
		sD = os.path.expanduser('~/Documents/cloud-files/')
		if not os.path.exists(sD): os.mkdir(sD)
		iS = int(self.headers['Content-length'])
		sR = ''
		while sR == '' or os.path.isfile(sD + sR):
			sR = ''.join((random.choice(string.letters + string.digits)) for i in range(60))
		with open(sD + sR, 'wb') as f:
			if iS > 0:
				iB = 512 * 1024
				while True:
					if iB > iS: iB = iS
					sB = self.rfile.read(iB)
					f.write(sB)
					iS -= len(sB)
					if iS <= 0: break
		self.send_response(200, 'OK')
		self.send_header('Content-length', '0')
		self.send_header('URL', sR)
		self.end_headers()
		
	def log_message(self, format, *args):
		pass
		
class DAVServer(HTTPServer):
	"""WebDAV server modified to mimic secret Gist"""
	def __init__(self, addr):
		HTTPServer.__init__(self, addr, DAVRequestHandler)
		
# --------------------

# coding: utf-8

import cloud, console, ui, threading
from PIL import Image

cloud.DAVurl = 'localhost'
s = cloud.DAVServer((cloud.DAVurl, 0))
cloud.DAVport = s.server_port
t = threading.Thread(target = s.serve_forever)
t.start()


with cloud.File('', 'w') as f:
	f.write('contents of file')
	url = f.commit()
with cloud.File(url, 'r') as f:
	console.hud_alert(f.read())
	
with cloud.File('', 'w', encryptionKey = 'password') as f:
	f.write('contents of encrypted file')
	url = f.commit()
with cloud.File(url, 'r', encryptionKey = 'password') as f:
	console.hud_alert(f.read())
	
	
v = ui.View()

with cloud.File('', 'wb') as f:
	ip = Image.open('iob:ios7_cloud_outline_256')
	ip.save(f, ip.format)
	url = f.commit()
with cloud.File(url, 'rb') as f:
	b1 = ui.Button(image = ui.Image.from_data(f.read()))
	v.add_subview(b1)
	
with cloud.File('', 'wb', encryptionKey = 'password') as f:
	ip = Image.open('iob:ios7_cloud_256')
	ip.save(f, ip.format)
	url = f.commit()
with cloud.File(url, 'rb', encryptionKey = 'password') as f:
	b2 = ui.Button(image = ui.Image.from_data(f.read()))
	b2.x = 300
	v.add_subview(b2)
	
v.present()
v.close()

# --------------------

