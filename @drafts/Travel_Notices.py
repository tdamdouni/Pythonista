import console
import sys
import webbrowser
import urllib
import os

base = "launchpro-messaging://"
to = "?to="
xcb = 'x-callback-url/'
body = "&body="
success = '&x-success='

INPUT_STRING = sys.argv[-1]


"""
Feel free to change these contacts to whomever you'd like to send
to send a message to
"""
contacts = [
    'friend1@gmail.com',
    'mom@gmail.com',
    '+1-555-555-5555',
    'friend2@gmail.com'
]

def quote(s, count=1):
    for i in range(count):
        s = urllib.quote(s, safe='') 
    return s

if INPUT_STRING == 'landed':
	land_location = console.input_alert("Location", "Where did you just land?")
	text = 'Just landed in %s' % land_location
if INPUT_STRING == 'boarding':
	text = 'Boarding now'
if INPUT_STRING == 'shuttingdown':
	text = 'Shutting down now'
	
text = text.encode('utf-8')
text = urllib.quote(text, safe='')

final_action = base + xcb + to + quote(contacts.pop(0)) + body + text + success
actions_list = [final_action]
for index, contact in enumerate(contacts):
    if len(contacts) == (index + 1):
        actions = base + to + contact + body + text
    else:
        actions = base + xcb + to + contact + body + text + success
    actions_list.append(actions)

for i in range(len(actions_list)):
    actions_list[i] = quote(actions_list[i], i)

webbrowser.open("".join(actions_list))