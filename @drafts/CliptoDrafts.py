#Summary: Takes copied text and creates new task in OmniFocus
#By: Jason Verly
#Rev: 2013-02-04
#Rev Note: Added Page Title & URL to clipped txt

import webbrowser
import clipboard
import urllib
import console
import sys

title = sys.argv[1]
url = sys.argv[2]

task = console.input_alert('Task', 'Enter task description')
task = urllib.quote(task)

note = clipboard.get()

full_note = ''.join([title,'\n\n', url, '\n\n', note])
full_note = urllib.quote(full_note.encode('utf-8'))

webbrowser.open('drafts4://x-callback-url/create?text=' + full_note)