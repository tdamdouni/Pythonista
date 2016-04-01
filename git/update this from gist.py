# Source: https://gist.github.com/Blether/7698491
#
# script to update current pythonista script from its github gist
# builds on the ole zorn gist download code
# uses first url found in the comments
#
# replaces old version ? better to elegant rename backup old version?

import clipboard
import editor
import console
import re
import os
from new_from_gist import download_gist

class InvalidGistURLError (Exception): pass
class MultipleFilesInGistError (Exception): pass
class NoFilesInGistError (Exception): pass
class GistDownloadError (Exception): pass

def first_url_from_comments(wholetext):
	first_url = ''
	for line in wholetext.splitlines():
		comment = re.findall(r"^#", line)
		if comment:
			match = re.findall(r"htt", line)
			if match:
				first_url = line[line.find('htt'):].split()[0]
				break 
	return first_url

def main():
	foo = editor.get_text()
	gist_url = first_url_from_comments(foo)
	try:
		filename, content = download_gist(gist_url)
		editor.replace_text(0,len(editor.get_text()),content)
		#else:
			#editor.make_new_file(filename, content)
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
	
