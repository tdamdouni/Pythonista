# Inspired by Dr. Drang's TextExpander snippet for adding iTunes affiliate code to URl. http://www.leancrew.com/all-this/2013/08/new-apple-affiliate-link-scripts/
# Modified for Pythonista. 

from sys import stdout
import clipboard, console, webbrowser, urllib

# My affiliate ID.
myID = '11l4RT'

tweetText = console.input_alert("", "Enter Tweet text.", "", "Awesome")

campaign = console.input_alert("", "Enter campaign flag for affiliate tracking.", "&ct=twitter", "Groovey")

# Get the URL from the clipboard.
clipURL = clipboard.get()

# Add myID and the partnerId parameter to the URL. If there are already
# queries, add them as additional ones; if not, add them as the only ones.
if '?' in clipURL:
  itemURL = '%s&at=%s%s' % (clipURL, myID, campaign)
else:
  itemURL = '%s?at=%s%s' % (clipURL, myID, campaign)

# Write to console
# console.clear()
# stdout.write(itemURL)

# Copy to clipboard
#clipboard.set(itemURL)

s = urllib.quote(itemURL.encode('utf-8'))
t = urllib.quote(tweetText.encode('utf-8'))


openLink = 'tweetbot://therotcod/post?text=' + t + '%0A%0A' + s

clipboard.set(itemURL)

webbrowser.open(openLink)
