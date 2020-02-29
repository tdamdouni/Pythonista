# coding: utf-8
'''Creates a zip archive of your Pythonista files and serves them via HTTP in your local network.'''
from __future__ import print_function

from SimpleHTTPServer import SimpleHTTPRequestHandler
from socket import gethostname, gethostbyname
import os
import shutil
import tempfile
import shutil

PORT = 8080

if __name__ == '__main__':
	doc_path = os.path.expanduser('~/Documents')
	os.chdir(doc_path)
	backup_path = os.path.join(doc_path, 'Backup.zip')
	if os.path.exists(backup_path):
		os.remove(backup_path)
	print('Creating backup archive...')
	shutil.make_archive(os.path.join(tempfile.gettempdir(), 'Backup'), 'zip')
	shutil.move(os.path.join(tempfile.gettempdir(), 'Backup.zip'), backup_path)
	print('Backup archive created, starting HTTP server...')
	from BaseHTTPServer import HTTPServer
	server = HTTPServer(('', PORT), SimpleHTTPRequestHandler)
	print('You can now download a backup of your Pythonista scripts bey entering this URL in a web browser on another device in your local network:')
	print('http://%s.local:%i/Backup.zip' % (gethostname(), PORT))
	print('Tap the stop button in the editor or console when you\'re done.')
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		server.shutdown()
		print('Server stopped')
