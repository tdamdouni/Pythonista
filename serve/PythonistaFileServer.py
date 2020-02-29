#! /usr/bin/env python

# https://gist.github.com/digitalrounin/c533d19ce0ada4738ecf

# File Transfer for Pythonista
# ============================
# This script allows you to transfer Python files from and to Pythonista via
# local Wifi.  It starts a basic HTTP server that you can access as a web page
# from your browser.  When you upload a file that already exists, it is renamed
# automatically.  From Pythonista's settings, you can add this script to the
# actions menu of the editor for quick access.
#
# Get Pythonista for iOS here:
#    http://omz-software.com/pythonista
#
# For the latest version of this script:
#    - https://github.com/digitalrounin/pythonista-fileserver
#
# -----------------------------------------------------------------------------
# By downloading or using the programs, you acknowledge acceptance of the
# following DISCLAIMER OF WARRANTY:
#
# DISCLAIMER OF WARRANTY
#
# ALL THE COMPUTER PROGRAMS AND SOFTWARE ARE PROVIDED "AS IS" WITHOUT WARRANTY
# OF ANY KIND. WE MAKE NO WARRANTIES, EXPRESS OR IMPLIED, THAT THEY ARE FREE OF
# ERROR, OR ARE CONSISTENT WITH ANY PARTICULAR STANDARD OF MERCHANTABILITY, OR
# THAT THEY WILL MEET YOUR REQUIREMENTS FOR ANY PARTICULAR APPLICATION. THEY
# SHOULD NOT BE RELIED ON FOR SOLVING A PROBLEM WHOSE INCORRECT SOLUTION COULD
# RESULT IN INJURY TO A PERSON OR LOSS OF PROPERTY. IF YOU DO USE THEM IN SUCH
# A MANNER, IT IS AT YOUR OWN RISK. THE AUTHOR AND PUBLISHER DISCLAIM ALL
# LIABILITY FOR DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES RESULTING FROM YOUR
# USE OF THE PROGRAMS.
# -----------------------------------------------------------------------------

# import console
# import editor
from __future__ import print_function
from os import path
import os

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from ConfigParser import SafeConfigParser
from cStringIO import StringIO
from socket import gethostname, gethostbyname, gaierror
import argparse
import base64
import cgi
import json
import mimetypes
import re
import ssl
import urllib
import urlparse


# Try and avoid manually changing this values, and use `config.cnf` instead.
# It will make future updates easier on you.
DEFAULT_CONFIG_DIR = '~/Documents/.httpfileserver'
DEFAULT_CONFIG_FILE = 'config.cfg'
DEFAULT_CONFIG = path.join(DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE)
CONFIG_SECTION = 'Pythonista File Server'
BUFFER_SIZE = 1048576
CONFIG_DEFAULTS = {
    'port': '8843',
    'protocol': 'https',
    'server_address': '',
    'auth_realm': 'Pythonista - File Server',
    'ssl_key': path.join(DEFAULT_CONFIG_DIR, 'server.key'),
    'ssl_crt': path.join(DEFAULT_CONFIG_DIR, 'server.crt'),
    'document_root': '~/Documents',
    'buffer_size': str(BUFFER_SIZE)}


def main():
	args = process_args()
	config = load_config(args.config_file)
	
	# console.clear()
	# pylint: disable=global-statement
	global BUFFER_SIZE
	BUFFER_SIZE = config.getint(CONFIG_SECTION, 'buffer_size')
	ssl_key_path = path.expanduser(config.get(CONFIG_SECTION, 'ssl_key'))
	ssl_crt_path = path.expanduser(config.get(CONFIG_SECTION, 'ssl_crt'))
	document_root = path.expanduser(
	config.get(CONFIG_SECTION, 'document_root'))
	print('SSL key file: {}'.format(ssl_key_path))
	print('SSL crt file: {}'.format(ssl_crt_path))
	print('Document root: {}'.format(document_root))
	
	user_key = base64.b64encode(
	'{}:{}'.format(config.get(CONFIG_SECTION, 'username'),
	config.get(CONFIG_SECTION, 'password')))
	
	port = config.getint(CONFIG_SECTION, 'port')
	server_address = config.get(CONFIG_SECTION, 'server_address')
	protocol = config.get(CONFIG_SECTION, 'protocol')
	server = FileServer(server_address=(server_address, port),
	RequestHandlerClass=FileServerRequestHandler,
	user_key=user_key,
	auth_realm=config.get(CONFIG_SECTION, 'auth_realm'),
	document_root=document_root)
	server.socket = ssl.wrap_socket(server.socket,
	keyfile=ssl_key_path,
	certfile=ssl_crt_path,
	server_side=True)
	
	url = '{0}://{1}:{2}'.format(protocol, get_my_address(), port)
	print('Open this page in your browser:')
	# console.set_font('Helvetica-Bold', 30)
	print(url)
	# console.set_font()
	print('Tap the stop button when you\'re done.')
	server.serve_forever()
	
	
def init_config(config_dir=DEFAULT_CONFIG_DIR):
	config_dir_path = path.abspath(path.expanduser(config_dir))
	if not path.exists(config_dir_path):
		print('Creating config directory: {}'.format(config_dir_path))
		os.makedirs(config_dir_path)
	else:
		print('Config directory already exists: {}'.format(config_dir_path))
		
	config_file_path = path.join(config_dir_path, DEFAULT_CONFIG_FILE)
	if not path.exists(config_file_path):
		print('Creating config file: {}'.format(config_file_path))
		config = load_config(config_file_path)
		config.add_section(CONFIG_SECTION)
		for name, value in config.items('DEFAULT'):
			config.set(CONFIG_SECTION, name, value)
			config.remove_option('DEFAULT', name)
		config.remove_section('DEFAULT')
		config.set(CONFIG_SECTION, 'username', '')
		config.set(CONFIG_SECTION, 'password', '')
		with open(config_file_path, 'w') as config_out:
			config.write(config_out)
		edit_config(config_file_path)
	else:
		print('Config file already exists: {}'.format(config_file_path))
		print('Use `HttpFileServer.edit_config()` to edit.')
		
		
def edit_config(config_file=DEFAULT_CONFIG):
	# pylint: disable=import-error
	config_file_path = path.abspath(path.expanduser(config_file))
	if path.exists(config_file_path):
		print('Opening: {}'.format(config_file_path))
		import editor
		editor.open_file(config_file_path)
	else:
		print('Config file does not exist: {}'.format(config_file_path))
		
		
def process_args():
	parser = argparse.ArgumentParser(
	description='Pythonista web server.')
	parser.add_argument(
	'--config',
	nargs='?',
	dest='config_file',
	default=DEFAULT_CONFIG,
	help='Configuration file to use.')
	return parser.parse_args()
	
	
def load_config(config_file):
	config_path = path.abspath(path.expanduser(config_file))
	config = SafeConfigParser(CONFIG_DEFAULTS)
	print('Loaded the following configration files: {}'\
	.format(config.read(config_path)))
	return config
	
	
def get_my_address():
	try:
		return gethostbyname('{}.local'.format(gethostname()))
	except gaierror:
		pass
		
	try:
		return gethostbyname(gethostname())
	except gaierror:
		pass
		
	return gethostname()
	
	
class FileServer(HTTPServer, object):
	def __init__(self, user_key, auth_realm, document_root, *args, **kwargs):
		self.user_key = user_key
		self.auth_realm = auth_realm
		self.document_root_abspath = path.abspath(document_root)
		super(FileServer, self).__init__(*args, **kwargs)
		
		
class FileServerRequestHandler(BaseHTTPRequestHandler, object):
	def __init__(self, *args, **kwargs):
		super(FileServerRequestHandler, self).__init__(*args, **kwargs)
		self.parsed_url = ""
		self.query_params = dict()
		self.request_path = ""
		self.document_root_abspath = ""
		self.request_abspath = ""
		
	def parse_request(self, *args, **kwargs):
		# Parse, validate, and authenticate the base request.
		if not (super(FileServerRequestHandler, self)
		.parse_request(*args, **kwargs)
		and self.authenticate()):
			return False
			
		# Extract more information
		self.parsed_url = urlparse.urlparse(self.path)
		self.query_params = urlparse.parse_qs(self.parsed_url.query)
		self.request_path = urllib.unquote(self.parsed_url.path)
		
		# Validate the path sent in the URL.
		if self.request_path != path.normpath(self.request_path):
			self.send_error(400, "Sketchy URL path sent")
			return False
			
		self.document_root_abspath = self.server.document_root_abspath
		self.request_abspath = path.abspath(
		path.join(self.document_root_abspath, self.request_path[1:]))
		
		return True
		
	def authenticate(self):
		auth_header = self.headers.getheader('Authorization')
		if auth_header == 'Basic {0}'.format(self.server.user_key):
			return True
		elif not auth_header:
			self.send_auth_header()
			self.wfile.write('No authentication header received.')
			return False
		else:
			self.send_auth_header()
			self.wfile.write(auth_header)
			self.wfile.write('not authenticated')
			return False
			
	def send_auth_header(self):
		self.send_response(401)
		self.send_header('WWW-Authenticate',
		'Basic realm=\"{0}\"'.format(self.server.auth_realm))
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		
	def do_HEAD(self):
		# pylint: disable=invalid-name
		print("send header")
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		
	def do_GET(self):
		# pylint: disable=invalid-name
		target = self.request_abspath
		if path.isdir(target):
			self.write_response()
		elif path.isfile(target):
			mime_type = mimetypes.guess_type(target, False)[0] \
			or 'application/octet-stream'
			self.send_response(200)
			self.send_header('Content-Type', mime_type)
			self.send_header('Content-Disposition',
			'attachment; filename={}'
			.format(path.basename(target)))
			self.end_headers()
			self.log_message('Sending: {}'.format(target))
			with open(target, 'rb') as in_file:
				stream_copy(in_file, self.wfile)
		else:
			self.write_response(
			code=404,
			alert_message='File not found.',
			alert_type='error')
			
	def do_POST(self):
		# pylint: disable=invalid-name
		form = cgi.FieldStorage(
		fp=self.rfile,
		headers=self.headers,
		environ={
		'REQUEST_METHOD': 'POST',
		'CONTENT_TYPE': self.headers['Content-Type']})
		
		uploaded_filename = form['file'].filename
		dest_path = self.get_unused_filename(uploaded_filename)
		self.log_message('Writing "{}" to: {}'
		.format(uploaded_filename, dest_path))
		with open(dest_path, 'wb') as output:
			stream_copy(form['file'].file, output)
			
		# editor.reload_files()
		dest_filename = path.relpath(dest_path, self.request_abspath)
		rename_message = ' (renamed to {})'.format(dest_filename) \
		if uploaded_filename != dest_filename \
		else ''
		message = '{} uploaded{}.'.format(uploaded_filename, rename_message)
		self.write_response(
		alert_message=message)
		
	def get_unused_filename(self, filename):
		# TODO - Validate filename?
		abs_path = path.abspath(
		path.join(self.request_abspath, filename))
		if not path.exists(abs_path):
			return abs_path
		elif self.query_flag('overwrite'):
			self.log_message('Overwriting: {}'.format(abs_path))
			return abs_path
			
		basename, ext = path.splitext(filename)
		regex = re.compile(r'^{}-(\d+){}$'
		.format(re.escape(basename), re.escape(ext)))
		matches = [regex.match(line)
		for line in os.listdir(self.request_abspath)]
		try:
			number = sorted([int(match.group(1))
			for match in matches if match])[-1] + 1
		except IndexError:
			number = 1
			
		return path.abspath(
		path.join(self.request_abspath,
		'{}-{}{}'.format(basename, number, ext)))
		
	def write_response(self,
	code=200,
	cwd=None,
	alert_message='success',
	alert_type='success'):
		cwd = cwd or self.request_path
		if 'text/html' in self.headers['Accept']:
			response_method = self.format_html_response
			content_type = 'text/html'
		else:
			response_method = self.format_json_response
			content_type = 'application/json'
		self.send_response(code)
		self.send_header('Content-Type', content_type)
		self.end_headers()
		self.wfile.write(response_method(
		cwd=cwd, alert_message=alert_message, alert_type=alert_type))
		
	def format_json_response(self, cwd, alert_message, alert_type):
		response = {
		'status': {
		'message': alert_message,
		'type': alert_type},
		'cwd': cwd}
		if not self.query_flag('short'):
			response['files'] = self.get_files()
		return json.dumps(response, indent=4, sort_keys=True)
		
	def query_flag(self, flag):
		return (flag in self.query_params) \
		and self.query_params[flag] \
		and self.query_params[flag][0].lower() == 'true'
		
	def format_html_response(self, cwd, alert_message, alert_type):
		if alert_message:
			alert_div = '<div class="alert alert-{0}">{1}</div>' \
			.format(alert_type, alert_message)
		else:
			alert_div = ''
		return TEMPLATE.format(alert_message=alert_div,
		file_list=self.get_html_file_list(),
		upload_path=cwd,
		bootstrap_css=BOOTSTRAP_CSS)
		
	def get_files(self):
		files = []
		for dirpath, _, filenames in os.walk(self.request_abspath):
			for filename in filenames:
				abs_path = path.abspath(path.join(dirpath, filename))
				rel_path = path.relpath(abs_path, self.document_root_abspath)
				files.append(rel_path)
		return files
		
	def get_html_file_list(self):
		string_buffer = StringIO()
		string_buffer.write('<ul>\n')
		for filename in self.get_files():
			string_buffer\
			.write('<li><a href="%s">%s</a></li>\n' % (filename, filename))
		string_buffer.write('</ul>\n')
		return string_buffer.getvalue()
		
		
def stream_copy(in_stream, out_stream):
	while True:
		chunk = in_stream.read(BUFFER_SIZE)
		if not chunk:
			break
		out_stream.write(chunk)
		
		
# pep8 noise
BOOTSTRAP_CSS = "https://netdna.bootstrapcdn.com/twitter-bootstrap/" \
    + "2.1.1/css/bootstrap-combined.min.css"
TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <link href="{bootstrap_css}" rel="stylesheet">
    </head>
    <body>
        <div class="navbar">
            <div class="navbar-inner">
                <a class="brand" href="#">Pythonista File Transfer</a>
            </div>
        </div>
        <div class="container">
            <h2>Upload File</h2>
            {alert_message}
            <p>
                <form action="{upload_path}"
                      method="POST"
                      enctype="multipart/form-data">
                    <div class="form-actions">
                        <input type="file" name="file"></input><br/><br/>
                        <button type="submit" class="btn btn-primary">
                            Upload
                        </button>
                    </div>
                </form>
            </p>
            <hr/>
            <h2>Download Files</h2>
            {file_list}
        </div>
    </body>
</html>
"""


if __name__ == '__main__':
	main()

