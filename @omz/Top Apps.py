# https://gist.github.com/omz/4034379

# Shows a list of the 10 top paid apps on the App Store.

print 'Loading...'

import feedparser
import console

print 'Fetching Feed...'
feed = feedparser.parse('http://itunes.apple.com/us/rss/toppaidapplications/limit=10/xml')
entries = feed['entries']
i = 1
console.clear()
print 'Top Paid Apps (US)\n'
for entry in entries:
	print str(i) + '. ' + entry['title']
	i += 1