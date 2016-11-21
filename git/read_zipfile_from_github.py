#!/usr/bin/env python3
# coding: utf-8

# https://github.com/cclauss/Ten-lines-or-less/blob/master/read_zipfile_from_github.py

# Pythonista appex script to copy and unpack a repo zipfile from GitHub

import appex, os, zipfile

if appex.is_running_extension():
	srce_path = appex.get_file_path()
	from_gh = os.path.abspath(os.path.expanduser('from GitHub'))
	os.makedirs(from_gh, exist_ok=True)
	with zipfile.ZipFile(srce_path) as zip_file:
		zip_file.extractall(from_gh)
	dir_name, _ = os.path.splitext(os.path.split(srce_path)[-1])
	msg = 'Files were unzipped into ~/'
	print(msg + os.path.relpath(os.path.join(from_gh, dir_name)))
else:  # Error handling...
	print('''=====
	* In Safari browser, navigate to a GitHub repo of interest.
	* Tap the green 'Clone or download' button.
	* Tap 'Download ZIP'.  (Big repos may take seveal seconds to download).
	* Tap 'Open in...'.
	* Tap 'Run Pythonista Script'.
	* Pick this script and tap the run button.
	* When you return to Pythonista the files should be in '~/from GitHub/'.''')

