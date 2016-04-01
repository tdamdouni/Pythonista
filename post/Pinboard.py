# https://gist.github.com/freekrai/4197073

import console
console.show_activity()
import urllib
from urllib import urlencode
import bs4
import requests
import webbrowser
import sys
import sound
sound.load_effect('Powerup_2')
import keychain
import clipboard
console.hide_activity()

numArgs = len(sys.argv)

if numArgs < 2:
    url = clipboard.get()

    console.show_activity()

    soup = bs4.BeautifulSoup(urllib.urlopen(url))
    title = soup.title.string
        text = title.encode('utf-8')

    console.hide_activity()

else:

    text = sys.argv[1]
    url = sys.argv[2]

PASSWORD = 'YOURPINBOARDPASSWORD'
USER = 'YOURPINBOARDUSERNAME'

tags = console.input_alert('Tags', 'Enter your tags below')

console.show_activity()

query = {'url': url,
         'description': text,
         'tags': tags}
query_string = urlencode(query)

pinboard_url = 'https://api.pinboard.in/v1/posts/add?' + query_string

r = requests.get(pinboard_url, auth=(USER, PASSWORD))

console.clear()

if r.status_code != 200:
    print 'Could not post:', r.text
    
elif r.status_code == 200:
    tags = tags.split(' ')
    tags = ','.join(tags)
    sound.play_effect('Powerup_2')
    print 'Link saved successfully'
    print text
    print "tags: " + tags