import clipboard
from console import alert
from json import loads
from sys import argv, exit
from urllib import urlopen
import webbrowser
 
def error_dialog(title, message):
	'''A diaolog box for error messages.'''
	try:
		alert(title, message)
	except KeyboardInterrupt:
		pass
	webbrowser.open('drafts://')
	exit(message)
 
def shorten_with_drngdk(long_url):
	'''basic link-shortening via drng.dk.'''
	api_url_base = 'http://api.drng.dk/create-link.php?url='
	try:
		response = urlopen(api_url_base + long_url)
	except IOError:
		error_dialog('Connection Error', 'Unable to perform request.')
	if response.getcode() == 200:
		jsonresponse = loads(response.read())
		short_link = jsonresponse['link']
		clipboard.set(short_link)
	else:
		error_dialog('Error', 'Status code: {0} - Message: {1}'.format(response.getcode(), response.read()))
	webbrowser.open('drafts://')
 
if __name__ == '__main__':
	shorten_with_drngdk(argv[1])
