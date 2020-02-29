# -*- coding: utf-8 -*-
from __future__ import print_function
import feedparser, webbrowser, urllib, console, sys, datetime, time
console.clear()
selected = "no"
notes = ""
now = datetime.datetime.now()
try:
	notes = sys.argv[2]
except:
	pass
header = "Music from today \n" # header
outp = "\n\n|Time|Track|\n|:---|:---|\n"
footer="#listened" # Gets appended to the entry
feedURL="http://ws.audioscrobbler.com/1.0/user/USERNAME/recenttracks.rss?limit=200&api_key=APIKEY" # Enter your user and API key. You can obtain the key for free at http://www.last.fm/api
for post in feedparser.parse(feedURL).entries:
	postDate = datetime.datetime.strptime(post.published[:-6], '%a, %d %b %Y %H:%M:%S') + datetime.timedelta(seconds = -time.timezone, hours = 1) # e.g. Sat, 12 Apr 2014 12:24:55 +0000
	timediff = now - postDate
	if timediff < datetime.timedelta(days = 1):
		# add to outp
		outp = outp + "|" + (datetime.datetime.strftime(postDate, '%H:%M')) + "|[" + post.title.replace("|","–") + "](" + post.link + ")|\n"
# User confirmation
print(outp)
if "preselect" in sys.argv:
	selected = "yes"
elif not raw_input("-- Press enter to import"):
	notes = raw_input("Any comments?")
	selected = "yes"
if selected == "yes":
	dayone_entry = header + notes + outp + footer
	# encode final entry
	dayone_entry = urllib.quote(dayone_entry.encode("utf-8"))
	webbrowser.open('dayone://post?entry=' + dayone_entry)
sys.exit()
