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
  # Open Drafts again.
  webbrowser.open('drafts://')
  exit(1)
 
def shorten_with_isgd(long_url):
  '''basic link-shortening via is.gd.'''
  api_base_url = 'http://is.gd/create.php?format=simple&url={url}'
  try:
    response = urlopen(api_url_base.formtat(url=long_url))
  except IOError:
    error_dialog('Connection Error', 'Unable to perform request.')
  if response.getcode() == 200:
    short_link = response.read()
	clipboard.set(short_link)
  else:
    error_dialog('Error', 'Status code: {0} - Message: {1}'.format(response.getcode(), response.read()))
  # Opening Drafts, the short-link is in the clipboard.
  webbrowser.open('drafts://')
 
if __name__ == '__main__':
  shorten_with_isgd(argv[1])