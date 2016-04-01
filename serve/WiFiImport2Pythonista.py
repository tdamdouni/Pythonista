# Contributed by OMZ here: https://gist.github.com/omz/3823483
# File Transfer for Pythonista
# ============================
# This script allows you to transfer Python files from
# and to Pythonista via local Wifi.
# It starts a basic HTTP server that you can access
# as a web page from your browser.
# When you upload a file that already exists, it is
# renamed automatically.
# From Pythonista's settings, you can add this script
# to the actions menu of the editor for quick access.
#
# Get Pythonista for iOS here:
# http://omz-software.com/pythonista

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import urllib
import cgi
import editor
import console
from socket import gethostname
import os
from cStringIO import StringIO

TEMPLATE = ('<!DOCTYPE html><html><head>' +
  '<link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/'+
  'css/bootstrap-combined.min.css" rel="stylesheet"></head><body>' +
  '<div class="navbar"><div class="navbar-inner">' +
  '<a class="brand" href="#">Pythonista File Transfer</a>' +
  '</div></div><div class="container">' +
  '<h2>Upload File</h2>{{ALERT}}'
  '<p><form action="/" method="POST" enctype="multipart/form-data">' +
  '<div class="form-actions">' +
  '<input type="file" name="file"></input><br/><br/>' +
  '<button type="submit" class="btn btn-primary">Upload</button>' +
  '</div></form></p><hr/><h2>Download Files</h2>' +
  '{{FILES}}</div></body></html>')

class TransferRequestHandler(BaseHTTPRequestHandler):
	def get_unused_filename(self, filename):
		if not os.path.exists(filename):
			return filename
		basename, ext = os.path.splitext(filename)
		suffix_n = 1
		while True:
			alt_name = basename + '-' + str(suffix_n) + ext
			if not os.path.exists(alt_name):
				return alt_name
			suffix_n += 1
	
	def get_html_file_list(self):
		buffer = StringIO()
		buffer.write('<ul>')
		files = os.listdir('.')
		for filename in files:
			if os.path.splitext(filename)[1] == '.py':
				buffer.write('<li><a href="%s">%s</a></li>' % (filename, filename))
		buffer.write('</ul>')
		return buffer.getvalue()
	
	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)
		path = parsed_path.path
		if path == '/':
			html = TEMPLATE
			html = html.replace('{{ALERT}}', '')
			html = html.replace('{{FILES}}', self.get_html_file_list())
			self.send_response(200)
			self.send_header('Content-Type', 'text/html')
			self.end_headers()
			self.wfile.write(html)
			return
		file_path = urllib.unquote(path)[1:]
		if os.path.isfile(file_path):
			self.send_response(200)
			self.send_header('Content-Type', 'application/x-python')
			self.send_header('Content-Disposition',
			                 'attachment; filename=%s' % file_path)
			self.end_headers()
			with open(file_path, 'r') as f:
				data = f.read()
				self.wfile.write(data)
		else:
			html = TEMPLATE
			html = html.replace('{{ALERT}}', 
			       '<div class="alert alert-error">File not found</div>')
			html = html.replace('{{FILES}}', self.get_html_file_list())
			self.send_response(404)
			self.send_header('Content-Type', 'text/html')
			self.end_headers()
			self.wfile.write(html)

	def do_POST(self):
		form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
		                        environ={'REQUEST_METHOD':'POST',
		                       'CONTENT_TYPE':self.headers['Content-Type']})
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		field_item = form['file']
		uploaded_filename = None
		dest_filename = None
		file_data = field_item.file.read()
		file_len = len(file_data)
		uploaded_filename = field_item.filename
		dest_filename = self.get_unused_filename(uploaded_filename)
		with open(dest_filename, 'w') as f:
			f.write(file_data)
		editor.reload_files()
		del file_data
		html = TEMPLATE
		if uploaded_filename != dest_filename:
			message = '%s uploaded (renamed to %s).' % (uploaded_filename,
			                                           dest_filename)
		else:
			message = '%s uploaded.' % (uploaded_filename)
		html = html.replace('{{ALERT}}',
		       '<div class="alert alert-success">%s</div>' % (message))
		html = html.replace('{{FILES}}', self.get_html_file_list())
		self.wfile.write(html)

if __name__ == '__main__':
	console.clear()
	from BaseHTTPServer import HTTPServer
	server = HTTPServer(('', 8080), TransferRequestHandler)
	URL = 'http://%s.local:8080' % gethostname()
	print 'Open this page in your browser:'
	console.set_font('Helvetica-Bold', 30)
	print URL
	console.set_font()
	print 'Tap the stop button when you\'re done.'
	server.serve_forever()
