# coding: utf-8

# This script downloads and opens a Gist from a URL in the clipboard.
# It's meant to be put in the editor's actions menu.
#
# It works with "raw" and "web" gist URLs, but not with gists that
# contain multiple files or non-Python files.
#
# If a file already exists, a dialog is shown that asks whether the
# new file should be renamed or replaced.

import appex
import clipboard
import console
import re
import os
import json

class InvalidGistURLError (Exception): pass
class MultipleFilesInGistError (Exception): pass
class NoFilesInGistError (Exception): pass
class GistDownloadError (Exception): pass

def test_filename(filename):
	if os.path.isfile(filename):
		return test_filename(console.input_alert('New File Name', 'Set the name of the Gist file', filename, 'OK', False))
	else:
		return filename
		
def download_gist(gist_url):
	# Returns a 2-tuple of filename and content
	
	console.show_activity()
	
	raw_match = re.match('http(s?)://raw.github.com/gist/', gist_url)
	if raw_match:
		import requests
		from urlparse import urlparse
		filename = os.path.split(urlparse(gist_url).path)[1]
		try:
			r = requests.get(gist_url)
			content = r.text
			return filename, content
		except:
			raise GistDownloadError()
	else:
		gist_id_match = re.match('http(s?)://gist.github.com/([0-9a-zA-Z]*)/([0-9a-f]*)', gist_url)
		if gist_id_match:
			import requests
			gist_id = gist_id_match.group(3)
			json_url = 'https://api.github.com/gists/' + gist_id
			try:
				gist_json = requests.get(json_url).text
				gist_info = json.loads(gist_json)
				files = gist_info['files']
			except:
				raise GistDownloadError()
			py_files = []
			for file_info in files.values():
				lang =  file_info.get('language', None)
				if lang != 'Python':
					continue
				py_files.append(file_info)
			if len(py_files) > 1:
				raise MultipleFilesInGistError()
			elif len(py_files) == 0:
				raise NoFilesInGistError()
			else:
				file_info = py_files[0]
				filename = file_info['filename']
				content = file_info['content']
				return filename, content
		else:
			raise InvalidGistURLError()
			
def main():
	if not appex.is_running_extension():
		gist_url = clipboard.get()
	else:
		gist_url = appex.get_url()
	try:
		filename, content = download_gist(gist_url)
		if os.path.isfile(filename):
			i = console.alert('File exists', 'A file with the name ' + filename +
			' already exists in your library.',
			'Rename','Replace')
			if i == 1:
				filename = test_filename(console.input_alert('New File Name', 'Set the name of the Gist file', filename, 'OK', False))
				
			try:
				import editor
				editor.make_new_file(filename, content)
			except ImportError:
				with open(filename, 'r+') as file:
					file.seek(0)
					file.write(content)
					file.truncate()
				console.hud_alert('Script added successfully', 'success')
				
		else:
			try:
				import editor
				editor.make_new_file(filename, content)
			except ImportError:
				with open(filename, 'a+') as file:
					file.seek(0)
					file.write(content)
					file.truncate()
				console.hud_alert('Script added successfully', 'success')
	except InvalidGistURLError:
		console.alert('No Gist URL',
		'The clipboard doesn\'t seem to contain a valid Gist URL.',
		'OK')
	except MultipleFilesInGistError:
		console.alert('Multiple Files', 'This Gist contains multiple ' +
		'Python files, which isn\'t currently supported.')
	except NoFilesInGistError:
		console.alert('No Python Files', 'This Gist contains no Python files.')
	except GistDownloadError:
		console.alert('Error', 'The Gist could not be downloaded.')
		
if __name__ == '__main__':
	main()

