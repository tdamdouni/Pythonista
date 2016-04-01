# coding: utf-8
from console import alert
from json import loads
from sys import exit
from urllib import urlopen, quote
import webbrowser
 
def error_dialog(title, message):
	'''A diaolog box for error messages.'''
	try:
		alert(title, message)
	except KeyboardInterrupt:
		pass
	webbrowser.open('drafts4://')
	exit(message)
 
def formatdate(date):
	'''bring the date into shape'''
	return date[:-1].replace('T', ' ')
 
def request(method):
	'''a request to github's status API.'''
	api_url_base = 'https://status.github.com/api/{method}'
	try:
		response = urlopen(api_url_base.format(method=method))
	except IOError:
		error_dialog('Connection Error', 'Unable to perform request.')
	if response.getcode() != 200:
		error_dialog('Error', 'Status code: {0} - Message: {1}'.format(response.getcode(), response.read()))
	return loads(response.read())
 
def github_status():
	'''get information and admin messages for github servers.'''
	status = request('status.json')
	messages = request('messages.json')
	output = '''
GITHUB STATUS
================
{date}: {status}
 
Last messages:
	'''.format(date=formatdate(status['last_updated']),
	           status=status['status'])
	for item in messages:
		output += '\n{date}: {status}\n{comment}\n'.format(date=formatdate(item['created_on']),
		                                                     status=item['status'],
		                                                     comment=item['body'])
	output += '\nFor further information: https://status.github.com/'
	webbrowser.open('drafts4://x-callback-url/create?text={0}'.format(quote(output)))
 
if __name__ == '__main__':
	github_status()