import feedparser
import time
import datetime
from dateutil import tz
import re
import httplib
import urllib
import os

HOME = os.path.expanduser('~')

DROPBOX_PERSONAL_FEED = ''
DROPBOX_WORK_FEED = ''

EVENT_THRESHOLD = 49


def pushover(title, message):
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                urllib.urlencode({
                    "token": "",
                    "user": "",
                    "title": title,
                    "message": message,
          }),{ "Content-type": "application/x-www-form-urlencoded" })


def is_deleted(entry):
    return True if 'deleted' in entry['summary'] else False


def cleanup(summary):
    return re.sub('<[^>]*>', '', summary)


def deletion_count(entry):
    deletion_search = re.search(
        r'and (?P<deletion_count>\d+) more files',
        entry['summary']
    )
    if deletion_search:
        return int(deletion_search.group('deletion_count'))
    else:
        return 1


def make_time(timestamp):
    from_zone = tz.gettz('GMT')
    to_zone = tz.tzlocal()

    dt = datetime.datetime.fromtimestamp(time.mktime(timestamp))
    local_time = dt.replace(tzinfo=from_zone)

    return local_time.astimezone(to_zone)

if __name__ == '__main__':
    for account in [DROPBOX_PERSONAL_FEED, DROPBOX_WORK_FEED]:
        to_ret = []
        d = feedparser.parse(account)
        for entry in d['entries']:
            if is_deleted(entry):
                to_ret.append(
                    dict(
                        entry=cleanup(entry['summary']),
                        date=make_time(entry['published_parsed']).strftime("%Y-%m-%d %H:%M:%S"),
                        deletion_count=deletion_count(entry),
                        id=entry['id']
                    )
                )

        LOG_PATH = os.path.join(HOME, 'logs', 'dropbox_events.log')
        if os.path.exists(LOG_PATH):
            already_logged = [line.replace('\n', '')
                              for line in open(LOG_PATH, 'r').readlines()]
        else:
            already_logged = []

        large_deletions = [entry for entry in to_ret
                           if entry['deletion_count'] >= EVENT_THRESHOLD
                           and entry['id'] not in already_logged]

        if large_deletions:
            pushover(
                '{count}Large {deletions} on Dropbox'.format(
                    count="%s " % len(large_deletions)
                    if len(large_deletions) > 1 else "",
                    deletions="Deletions"
                    if len(large_deletions) > 1 else "Deletion"),
                large_deletions[0]['entry']
            )
            for large_deletion in large_deletions:
                with open(LOG_PATH, 'a') as f:
                    f.write("%s\n" % large_deletion['id'])



