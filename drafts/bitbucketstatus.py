from console import alert
import feedparser
from sys import exit
from urllib import urlopen, quote
import webbrowser
 
def error_dialog(title, message):
	'''A diaolog box for error messages.'''
	try:
		alert(title, message)
	except KeyboardInterrupt:
		pass
	webbrowser.open('drafts://')
	exit(message)
 
def request():
	'''a request to bitbuckets status feed.'''
	api_url_base = 'http://feeds.feedburner.com/BitBucketServerStatus'
	try:
		response = urlopen(api_url_base)
	except IOError:
		error_dialog('Connection Error', 'Unable to perform request.')
	if response.getcode() != 200:
		error_dialog('Error', 'Status code: {0} - Message: {1}'.format(response.getcode(), response.read()))
	return response.read()
 
def bitbucket_status():
	'''get information and admin messages for bitbucket servers from bitbucket feed.'''
	bitbucket_feed = request()
	feed = feedparser.parse(bitbucket_feed)
	output = '''
{title}
================
Last entries:
	'''.format(title=feed['feed']['title'])
	for entry in feed['entries']:
		output += '\n{date}: {comment}\n'.format(date=entry['title'],
		                                         comment=entry['summary_detail']['value'])
	output += '\nFor further information: http://status.bitbucket.org/'
	webbrowser.open('drafts://x-callback-url/create?text={0}'.format(quote(output)))
 
if __name__ == '__main__':
	bitbucket_status()