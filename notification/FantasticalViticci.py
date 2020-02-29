#coding: utf-8
# Original script by Federico Viticci:
# http://www.macstories.net/reviews/fantastical-for-iphone-review/
# Modified to work better with international characters

from __future__ import print_function
import webbrowser
import clipboard
import urllib
import console

when = clipboard.get()

fant = 'fantastical://parse?sentence='

newtask = console.input_alert('What is this?', 'Type your event below')

loc = console.alert('Location', 'Does the event have a location?', 'Yes', 'No')

if loc == 1:
	place = console.input_alert('Where', 'Type your location below')

	event = newtask.decode('utf-8') + ' ' + when + ' at ' + place.decode('utf-8')

	encoded = urllib.quote(event.encode('utf-8'), safe='')
	
elif loc == 2:
	event = newtask.decode('utf-8') + ' ' + when
	print(type(event))
	encoded = urllib.quote(event.encode('utf-8'), safe='')
	
text = fant + encoded

webbrowser.open(text)
