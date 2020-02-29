#!/usr/bin/env python
# coding=utf8

# http://leancrew.com/all-this/2016/05/date-without-time-stamps/

from __future__ import print_function
import feedparser as fp
import time
from datetime import datetime, timedelta
import pytz

subscriptions = [
  'http://feedpress.me/512pixels',
  'http://www.leancrew.com/all-this/feed/',
  'http://ihnatko.com/feed/',
  'http://blog.ashleynh.me/feed',
  'http://www.betalogue.com/feed/',
  'http://bitsplitting.org/feed/',
  'http://feedpress.me/jxpx777',
  'http://kieranhealy.org/blog/index.xml',
  'http://blueplaid.net/news?format=rss',
  'http://brett.trpstra.net/brettterpstra',
  'http://feeds.feedburner.com/NerdGap',
  'http://www.libertypages.com/clarktech/?feed=rss2',
  'http://feeds.feedburner.com/CommonplaceCartography',
  'http://kk.org/cooltools/feed',
  'http://danstan.com/blog/imHotep/files/page0.xml',
  'http://daringfireball.net/feeds/main',
  'http://david-smith.org/atom.xml',
  'http://feeds.feedburner.com/drbunsenblog',
  'http://stratechery.com/feed/',
  'http://www.gnuplotting.org/feed/',
  'http://feeds.feedburner.com/jblanton',
  'http://feeds.feedburner.com/IgnoreTheCode',
  'http://indiestack.com/feed/',
  'http://feedpress.me/inessential',
  'http://feeds.feedburner.com/theendeavour',
  'http://feed.katiefloyd.me/',
  'http://feeds.feedburner.com/KevinDrum',
  'http://www.kungfugrippe.com/rss',
  'http://lancemannion.typepad.com/lance_mannion/rss.xml',
  'http://www.caseyliss.com/rss',
  'http://www.macdrifter.com/feeds/all.atom.xml',
  'http://mackenab.com/feed',
  'http://hints.macworld.com/backend/osxhints.rss',
  'http://macsparky.com/blog?format=rss',
  'http://www.macstories.net/feed/',
  'http://www.marco.org/rss',
  'http://merrillmarkoe.com/feed',
  'http://mjtsai.com/blog/feed/',
  'http://feeds.feedburner.com/mygeekdaddy',
  'http://nathangrigg.net/feed.rss',
  'http://onethingwell.org/rss',
  'http://schmeiser.typepad.com/penny_wiseacre/rss.xml',
  'http://www.practicallyefficient.com/feed.xml',
  'http://robjwells.com/rss',
  'http://www.red-sweater.com/blog/feed/',
  'http://blog.rtwilson.com/feed/',
  'http://feedpress.me/sixcolors',
  'http://feedpress.me/candlerblog',
  'http://inversesquare.wordpress.com/feed/',
  'http://high90.com/feed',
  'http://joe-steel.com/feed',
  'http://feeds.veritrope.com/',
  'http://xkcd.com/atom.xml',
  'http://doingthatwrong.com/?format=rss']

# Date and time setup. I want only posts from today,
# where "today" starts at 10 PM of the previous day and
# lasts until 2 AM of the following day.
# Exception: if the entry's date is today with a timestamp
# of exactly midnight (00:00:00), include that, too, even
# if its timezone is UTC, as that probably represents a
# datestamp of today without a real timestamp.
utc = pytz.utc
homeTZ = pytz.timezone('US/Central')
mnToday = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
dt = datetime.now(homeTZ)
if dt.hour < 2:
  dt -= timedelta(hours=48)
else:
  dt -= timedelta(hours=24)
start = dt.replace(hour=22, minute=0, second=0, microsecond=0)
start = start.astimezone(utc)


# Collect all of today's posts and put them in a list of tuples.
posts = []
for s in subscriptions:
  f = fp.parse(s)
  try:
    blog = f['feed']['title']
  except KeyError:
    continue
  for e in f['entries']:
    try:
      when = e['published_parsed']
    except KeyError:
      when = e['updated_parsed']
    when =  datetime(*when[:6])
    # This is the exception. Change it to midnight today, local time.
    if when == mnToday:
      when = homeTZ.localize(when).astimezone(utc)
    else:
      when = utc.localize(when)
    if when > start:
      title = e['title']
      try:
        body = e['content'][0]['value']
      except KeyError:
        body = e['summary']
      link = e['link']
      posts.append((when, blog, title, link, body))

# Sort the posts in reverse chronological order.
posts.sort()
posts.reverse()

# Turn them into an HTML list.
listTemplate = '''<li>
  <p class="title"><a href="{3}">{2}</a></p>
  <p class="info">{1}<br />{0}</p>
  <p>{4}</p>\n</li>'''
litems = []
for p in posts:
  q = [ x.encode('utf8') for x in p[1:] ]
  timestamp = p[0].astimezone(homeTZ)
  q.insert(0, timestamp.strftime('%b %d, %Y %I:%M %p'))
  litems.append(listTemplate.format(*q))
ul = '\n<hr />\n'.join(litems)

# Print the HTMl.
print('''<html>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width" />
<head>
<style>
body {{
  background-color: #555;
  width: 750px;
  margin-top: 0;
  margin-left: auto;
  margin-right: auto;
  padding-top: 0;
}}
h1, h2, h3, h4, h5, h6 {{
  font-family: Helvetica, Sans-serif;
}}
h1 {{
  font-size: 110%;
}}
h2 {{
  font-size: 105%;
}}
h3, h4, h5, h6 {{
  font-size: 100%;
}}
.rss {{
  list-style-type: none;
  margin: 0;
  padding: .5em 1em 1em 1.5em;
  background-color: white;
}}
.rss li {{
  margin-left: -.5em;
  line-height: 1.4;
}}
.rss li pre {{
  overflow: auto;
}}
.rss li p {{
  overflow-wrap: break-word;
  word-wrap: break-word;
  word-break: break-word;
  -webkit-hyphens: auto;
  hyphens: auto;
}}
.rss li figure {{
  -webkit-margin-before: 0;
  -webkit-margin-after: 0;
  -webkit-margin-start: 0;
  -webkit-margin-end: 0;
}}
.title {{
  font-weight: bold;
  font-family: Helvetica, Sans-serif;
  font-size: 120%;
  margin-bottom: .25em;
}}
.title a {{
  text-decoration: none;
  color: black;
}}
.info {{
  font-size: 85%;
  margin-top: 0;
  margin-left: .5em;
}}
img {{
  max-width: 700px;
}}
@media screen and (max-width:667px) {{
  body {{
    font-size: 200%;
    width: 650px;
    background-color: white;
  }}
  .rss li {{
    line-height: normal;
  }}
  img {{
    max-width: 600px;
  }}
}}
</style>
<title>Today’s RSS</title>
<body>
<ul class="rss">
{}
</ul>
</body>
</html>
'''.format(ul))
