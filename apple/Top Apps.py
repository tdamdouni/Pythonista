# Shows a list of the 10 top paid apps on the App Store.

print 'Loading...\n'

import feedparser
import console

print 'Fetching Feed...\n'
feed = feedparser.parse('http://itunes.apple.com/de/rss/toppaidapplications/limit=10/xml')
entries = feed['entries']
i = 1
console.clear()
print 'Top Paid Apps (DE)\n'
for entry in entries:
	print str(i) + '. ' + entry['title']
	i += 1