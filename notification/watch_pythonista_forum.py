# coding: utf-8

# https://gist.github.com/cclauss/8794104

# Learning how to use feedparser... recent_entries() will print out info on all posts to the Pythonista forum in the past 24 hours. watch_feed() will print out info on the last post to the Pythonista forum. Sleeps for 15 minutes then check to see if there is a newer post. If so, prints out info on it and opens its URL in the webbrowser. Repeat.

#!/usr/bin/env python

'''
recent_entries() will print out info on all posts to the Pythonista forum in the past 24 hours.

watch_feed() will print out info on the last post to the Pythonista forum.
Sleeps for 15 minutes then check to see if there is a newer post.
If so, prints out info on it and opens its URL in the webbrowser.  Repeat.
'''

import datetime, feedparser, sys, time, webbrowser

feed_url = 'http://omz-forums.appspot.com/pythonista/rss'
feed_fmt = '''{title} -- {published}
>>> {link}
>>> {summary}'''

def get_latest_entry(in_url = feed_url):
    rss_entry = feedparser.parse(feed_url).entries
    return rss_entry[0] if rss_entry else None

def watch_feed(in_url = feed_url, in_sleep_minutes = 15):
    prev_post = get_latest_entry(in_url)
    if prev_post:
        # import pprint ; pprint.pprint(prev_post)
        print(feed_fmt.format(**prev_post))
    while prev_post:
        curr_post = get_latest_entry(in_url)
        if curr_post and curr_post != prev_post:
            print(feed_fmt.format(**curr_post))
            webbrowser.open(curr_post.link)  # open new post in browser
            prev_post = curr_post
        print('{} --- sleeping... {}'.format(time.ctime(), '-' * 20))
        for i in xrange(in_sleep_minutes * 6):  # in Pythonista, allow the
            time.sleep(10)  # user to halt the script once every 10 seconds
        # probably add nodoze.py here to wake up device if it goes to sleep

def hours_ago(in_hours_ago = 24):
    delta_t = datetime.timedelta(hours=in_hours_ago)
    return time.time() - delta_t.total_seconds()

def recent_entries(in_url = feed_url, in_hours_ago = 24):
    cutoff_time = hours_ago(in_hours_ago)
    print('=' * 40)
    print('Cutoff time is: {}'.format(time.ctime(cutoff_time)))
    cutoff_time = time.gmtime(cutoff_time)  # struct_time
    rss_entries = feedparser.parse(in_url).entries
    # import pprint ; pprint.pprint(rss_entries[0])
    for i, post in enumerate(rss_entries):
        post_time = time.strptime(post['published'], '%a, %d %b %Y %H:%M:%S')
        if post_time < cutoff_time:  # this post is too old
            return rss_entries[:i]   # return entries before cutoff_time
    return rss_entries  # ALL entries are before cutoff_time

def main(argv):
    rss_entries = recent_entries(feed_url, 24)
    if not rss_entries:
        print('No new entries in the past 24 hours!!')
    for the_post in rss_entries:
        print('-' * 20)
        # import pprint ; pprint.pprint(the_post)
        print(feed_fmt.format(**the_post))
    for i in xrange(2):
        print('=' * 40)
    watch_feed(feed_url)

if __name__ == '__main__':
    sys.exit(main(sys.argv))