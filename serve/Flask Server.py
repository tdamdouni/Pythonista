# coding= utf-8

# https://gist.github.com/anonymous/5243230

# https://forum.omz-software.com/topic/1412/pypi-installer-and-web-server

from flask import Flask, request
import socket
from Pypi import Installer
app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello World!'
	
@app.route('/install')
def install():
	package = request.args.get('package', '')
	version = request.args.get('version', '')
	i = Installer(package, version)
	i.install()
	return 'Successfully installed ' + package

# Attempt at getting this device's ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('www.google.com', 9))
print 'My IP: ' + s.getsockname()[0]
s.close()

app.run(host='0.0.0.0')