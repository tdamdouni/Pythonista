from __future__ import print_function
# https://gist.github.com/lukf/9785293

# -*- coding: utf-8 -*-
import feedparser, webbrowser, urllib, console, sys, datetime, urllib2, time
console.clear()
selected = "no"
feedURL="http://feeds.pinboard.in/rss/secret:YOURSECRET/u:USERNAME/" # RSS feed URL
outp="Bookmarks from today \n|Time|Page|Tags|\n|:---|:---|:---|\n" # header
dayone_footer="#bookmark" # Gets appended to the entry
now = datetime.datetime.now()
for post in feedparser.parse(urllib2.urlopen(feedURL).read().replace('dc:subject>', 'subject>')).entries:
	postDate = datetime.datetime.strptime(post.date[:-6], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(seconds = -time.timezone, hours = 1) # 2014-04-10T15:00:01+00:00
	timediff = now - postDate 
	if timediff < datetime.timedelta(days = 1):
		# add to outp
		subject = ""
		try:
			subject = "#" + post.subject.replace(' ', ' #')
		except:
			pass
		outp = outp + "|" + (datetime.datetime.strftime(postDate, '%H:%M')) + "|" + "[" + post.title.replace('[priv] ','').replace('|','–')  + "](" + post.link + ")|" + subject + "|\n"
		
dayone_entry=outp+dayone_footer
# User confirmation
print(dayone_entry)
if "preselect" in sys.argv:
	selected = "yes"
elif not raw_input("-- Press enter to import"):
	selected = "yes"
	# encode final entry
if selected == "yes":
	dayone_entry = urllib.quote(dayone_entry.encode("utf-8"))
	webbrowser.open('dayone://post?entry='+dayone_entry)
sys.exit()
