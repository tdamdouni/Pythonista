# https://gist.github.com/lukf/10540780

# -*- coding: utf-8 -*-
import console, datetime, feedparser, sys, time, urllib, webbrowser
# Enter your user and API key below. You can obtain the key for free at http://www.last.fm/api
feedURL="http://ws.audioscrobbler.com/1.0/user/USERNAME/recenttracks.rss?limit=200&api_key=APIKEY"

console.clear()
now = datetime.datetime.now()
outp = ''
for post in feedparser.parse(feedURL).entries:
    postDate = datetime.datetime.strptime(post.published[:-6], '%a, %d %b %Y %H:%M:%S') + datetime.timedelta(seconds = -time.timezone, hours = 1) # e.g. Sat, 12 Apr 2014 12:24:55 +0000
    timediff = now - postDate
    if timediff < datetime.timedelta(days = 1):
        # add to outp
        outp += '|{}|[{}]({})|\n'.format(datetime.datetime.strftime(postDate, '%H:%M'),
                                         post.title.replace("|","–"),
                                         post.link)
if not outp:
    sys.exit('No output.')

# User confirmation
print(outp)
dayone_entry = '''Music from today {}\n\n
|Time|Track|
|:---|:---|
{}
#listened'''
notes = sys.argv[2] if len(sys.argv) > 2 else ''
selected = False
if "preselect" in sys.argv:
    selected = True
elif not raw_input("-- Press enter to import"):
    notes = raw_input("Any comments?")
    selected = True
if selected:
    dayone_entry = dayone_entry.format(notes, outp)
    # encode final entry
    dayone_entry = urllib.quote(dayone_entry.encode("utf-8"))
    webbrowser.open('dayone://post?entry=' + dayone_entry)
