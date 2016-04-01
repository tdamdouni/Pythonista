# coding: utf-8

# http://mygeekdaddy.net/2014/03/03/fixing-my-gtd-system/

import webbrowser
import clipboard
import urllib
import sys

title = sys.argv[1]
url = sys.argv[2]
note = clipboard.get()

full_note = ''.join([title,'\n\n', url, '\n\n', note])
full_note = urllib.quote(full_note.encode('utf-8'))

webbrowser.open('drafts4://x-callback-url/create?text=' + full_note)