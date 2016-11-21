# https://forum.omz-software.com/topic/3326/share-code-serving-files-over-http

import os
import shutil
import socket
import urllib.parse

import dialogs
import editor
import flask


# SETUP


# Resolve local IP by connecting to Google's DNS server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localip = s.getsockname()[0]
s.close()


# Initialize Flask
app = flask.Flask(__name__)

# Calculate path details
directory, filename = os.path.split(editor.get_path())
dirpath, dirname = os.path.split(directory.rstrip("/"))
zippath = os.path.abspath("./{}.zip".format(dirname))

# Make an archive
shutil.make_archive(dirname, "zip", dirpath, dirname)


# Configure server routings
@app.route("/")
def index():
	"""Serve a zip of it all from the root"""
	return flask.send_file(zippath)
	
	
@app.route("/<path:path>")
def serve_file(path):
	"""Serve individual files from elsewhere"""
	return flask.send_from_directory(directory, path)
	
# Run the app
print("Running at {}".format(localip))
app.run(host="0.0.0.0", port=80)

# After it finishes
os.remove(zippath)
# --------------------

