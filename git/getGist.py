# coding: utf-8

# This script downloads and opens a Gist from a URL in the clipboard.
# It's meant to be put in the editor's actions menu.
#
# It works with "raw" and "web" gist URLs, but not with non-Python files.
#
# If a file already exists, a dialog is shown that asks whether the
# new file should be renamed automatically.

# https://gist.github.com/silarsis/4036200

import sys
import clipboard
import editor
import console
import re
import os

class InvalidGistURLError (Exception): pass
class NoFilesInGistError (Exception): pass
class GistDownloadError (Exception): pass

def download_gist(gist_url):
	# Returns a 2-tuple of filename and content
	# console.show_activity()
	raw_match = re.match('http(s?)://raw.github.com/gist/', gist_url)
	if raw_match:
		import requests
		from urlparse import urlparse
		filename = os.path.split(urlparse(gist_url).path)[1]
		try:
			r = requests.get(gist_url)
			content = r.text
			yield filename, content
		except:
			raise GistDownloadError()
	else:
		gist_id_match = re.match('http(s?)://gist.github.com/([0-9a-f]*)', gist_url)
		if gist_id_match:
			import requests
			gist_id = gist_id_match.group(2)
			json_url = 'https://api.github.com/gists/' + gist_id
			try:
				import json
				gist_json = requests.get(json_url).text
				gist_info = json.loads(gist_json)
				files = gist_info['files']
			except:
				raise GistDownloadError()
			for file_info in files.values():
				lang =  file_info.get('language', None)
				if lang != 'Python':
					continue
				filename = file_info['filename']
				content = file_info['content']
				yield filename, content
		else:
			raise InvalidGistURLError()
			
def main():
	gist_url = clipboard.get()
	num = 0
	try:
		for num, (filename, content) in enumerate(download_gist(gist_url), start=1):
			if os.path.isfile(filename):
				i = console.alert('File exists', 'A file with the name ' + filename +
				' already exists in your library.',
				'Auto Rename', 'Skip')
				if i == 1:
					editor.make_new_file(filename, content)
			else:
				editor.make_new_file(filename, content)
	except InvalidGistURLError:
		console.alert('No Gist URL',
		'The clipboard doesn\'t seem to contain a valid Gist URL.',
		'OK')
	except GistDownloadError:
		console.alert('Error', 'The Gist could not be downloaded.')
	if not num:
		console.alert('No Python Files', 'This Gist contains no Python files.')
		
if __name__ == '__main__':
	main()

