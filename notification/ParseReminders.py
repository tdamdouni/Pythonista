# coding: utf-8

# http://unapologetic.io/posts/2013/10/30/the-parse-reminders-in-fantastical-action/

import webbrowser
import urllib
import sys

reminders = sys.argv[1]
i = 0
while i < len(reminders):
    if reminders[i] == ',':
        reminders = reminders[0:i] + '\n\n' + reminders[i+1:len(reminders)]
    i += 1

reminders = reminders.encode('utf-8')
reminders = urllib.quote(reminders, safe='')

base = 'drafts4://x-callback-url/create?text=' + reminders + '&action=Parse%20Reminders%20In%20Fantastical'


webbrowser.open(base)