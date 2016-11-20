# coding: utf-8

[youtubearchiving]: https://github.com/lukaskollmer/pythonista-scripts/tree/master/youtube_archiving

import re
import sys
import appex
import console
import datetime
import clipboard
import urllib2


#clipboard.set('https://youtu.be/fTTGALaRZoc')

add_if_already_exists = False

console.clear()


import LKEvernoteApi


def title_of_url(url):
  try:
    soup = BeautifulSoup(urllib2.urlopen(url))
    return soup.title.string
  except:  # caution: avoid naked exceptions
    return ''


guid = '__YOUR_NOTE_GUID_HERE__'

user_input = ''  # input is a built-in function so use a different name

if appex.is_running_extension():
	LKEvernoteApi.log_progress('load url provided to app extension')
	user_input = appex.get_url()
else:
	LKEvernoteApi.log_progress('not running from extension, checking arguments')
	if len(sys.argv) > 1:
		evernote.log_progress('argument found, use that')
		user_input = sys.argv[1]
	else:
		LKEvernoteApi.log_progress('no arguments found, will use clipboard text')
		user_input = clipboard.get()
		if not user_input:
			sys.exit('Clipboard is empty, no arguments passed to script')

LKEvernoteApi.log_progress('Loading title of passed url')
url_title = title_of_url(user_input)
if url_title:
	url_title = ' ({}) '.format(url_title.replace('&', 'and'))

LKEvernoteApi.log_progress('create ENML string')
fmt = '<en-todo checked="false"></en-todo> {}{}(@ {:%d %b %Y %H:%M})'
en_todo_text = fmt.format(input, url_title, datetime.datetime.now())
print(en_todo_text)

LKEvernoteApi.log_progress('call ´appendNote´ function')
LKEvernoteApi.append_to_note(guid=guid, new_content=en_todo_text, main_new_content=user_input,
			     add_if_already_exists=add_if_already_exists)

LKEvernoteApi.log_progress('Done')

if appex.is_running_extension():
	appex.finish()
	#utilities.quit()
else:
	sys.exit()
