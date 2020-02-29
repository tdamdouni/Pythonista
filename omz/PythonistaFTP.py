# https://gist.github.com/omz/1aec8a66a5d5d19a36ab

'''FTP server for Pythonista (iOS)

You can use this to exchange files with a Mac/PC or a file management app on the same device (e.g. Transmit).

If you use a Mac, you can connect from the Finder, using the "Go -> Connect to Server..." menu item.
'''
from __future__ import print_function

import os
from socket import gethostname

def install_pyftpdlib():
	print('Downloading pyftpdlib...')
	import urllib
	import shutil
	os.chdir(os.path.expanduser('~/Documents'))
	urllib.urlretrieve('https://pypi.python.org/packages/source/p/pyftpdlib/pyftpdlib-1.4.0.tar.gz', 'pyftpd.tar.gz')
	import tarfile
	t = tarfile.open('pyftpd.tar.gz')
	t.extractall()
	shutil.copytree('pyftpdlib-1.4.0/pyftpdlib', 'site-packages/pyftpdlib')
	shutil.rmtree('pyftpdlib-1.4.0')
	os.remove('pyftpd.tar.gz')
	
try:
	import pyftpdlib
except ImportError:
	install_pyftpdlib()

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading

def main():
	authorizer = DummyAuthorizer()
	authorizer.add_anonymous(os.path.expanduser('~/Documents'), perm='elradfmwM')
	handler = FTPHandler
	handler.authorizer = authorizer
	server = FTPServer(('0.0.0.0', 2121), handler)
	t = threading.Thread(target=server.serve_forever)
	t.start()
	print('Server started.')
	print('\nConnect as guest/anonymous user to ftp://localhost:2121 (from this device) or "ftp://(YOUR_IP_ADDRESS):2121" (from other devices in your network -- you can find the IP address of your device in the WiFi settings)')
	try:
		while True: pass
	except KeyboardInterrupt:
		server.close_all()
		print('Server stopped')

if __name__ == '__main__':
	main()