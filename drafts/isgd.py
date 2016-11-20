# https://gist.github.com/kultprok/f4f62e4e9bc59e575726
# http://kulturproktologie.de/?p=4602
import clipboard
from console import alert
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

def shorten_with_isgd(long_url):
	'''basic link-shortening via is.gd.'''
	api_url_base = 'http://is.gd/create.php?format=simple&url='
	try:
		response = urlopen(api_url_base + long_url)
	except IOError:
		error_dialog('Connection Error', 'Unable to perform request.')
	if response.getcode() == 200:
		short_link = response.read()
		clipboard.set(short_link)
	else:
		error_dialog('Error', 'Status code: {0} - Message: {1}'.format(response.getcode(), response.read()))
	webbrowser.open('drafts://')

if __name__ == '__main__':
	shorten_with_isgd(argv[1])
