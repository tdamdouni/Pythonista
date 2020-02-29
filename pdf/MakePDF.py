from __future__ import print_function
# Original script by Federico Viticci:
# http://omz-software.com/pythonista/forums/discussion/comment/165#Comment_165

# dropboxlogin must be setup prior to using this script
# Script by OMZ located here: https://gist.github.com/4034526

# javascript:window.location='pythonista://MakePDF?action=run&argv='+encodeURIComponent(document.title)+'&argv='+encodeURIComponent(document.location.href);


import clipboard
import urllib2
import console
from dropboxlogin import get_client
dropbox_client = get_client()
import keychain
import time
import webbrowser
import sys
import webbrowser
import urllib
import bs4

numArgs = len(sys.argv)

console.clear()

if numArgs < 2:
    url = clipboard.get()
    console.show_activity()

    soup = bs4.BeautifulSoup(urllib.urlopen(url))
    title = soup.title.string
    name = title.encode('utf-8')

    console.hide_activity()
    
else:
    webpage = sys.argv[1]
    name = webpage.encode('utf-8')
    url = sys.argv[2]

insta = 'http://instapaper.com/text?u='

URL = insta + url

print('Generating HTML file...')

getText = urllib2.Request(URL)
openText = urllib2.urlopen(getText)
content = (openText.read().decode('utf-8'))

final = content.encode('utf-8')

print('Uploading HTML file to Dropbox...')


response = dropbox_client.put_file('/' + name + '.html', final)

print('Your HTML file has been uploaded')