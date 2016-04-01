import requests
import json

# Make it a bit prettier..
print "-" * 30
print "This will show the Most Popular Videos on YouTube"
print "-" * 30

# Get the feed
#r = requests.get("http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?v=2&alt=jsonc")
r = requests.get("http://gdata.youtube.com/feeds/api/standardfeeds/most_recent?v=2&alt=jsonc")
r.text

# Convert it to a Python dictionary
data = json.loads(r.text)

# Save into a separate dictionary to sort by view count
sdata = {}
for item in data['data']['items']:
    title = item['title'].encode('ascii','ignore')
    category = item['category']
    id = item['id']
    rating = item['rating']
    url = item['player']['default']
    viewCount = item['viewCount']
    duration = item['duration']
    new = {
        'title' : title,
        'category' : category,
        'id' : id,
        'rating' : rating,
        'url' : url,
        'viewCount' : viewCount,
        'duration' : duration
    }
    sdata[viewCount] = new


# Loop through the result.
for item in sorted(sdata.keys(), reverse=True):
    print "Video Title: %s" % (sdata[item]['title'].encode('ascii','ignore'))
    print "Video Category: %s" % (sdata[item]['category'])
    print "Video ID: %s" % (sdata[item]['id'])
    print "Video Rating: %f" % (sdata[item]['rating'])
    print "Embed URL: %s" % (sdata[item]['url'])
    print "View Count: {:,}".format(sdata[item]['viewCount'])
    print "Duration: %d" % (sdata[item]['duration'])
    print 
