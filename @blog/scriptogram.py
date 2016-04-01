#!/usr/bin/env python

import os
import sys
from datetime import datetime
import requests
from time import sleep

HOME = os.path.expanduser('~')

# Put all the paths you want the script to watch.
# I recommend putting names at the end, so you can 
# know who made the post. See also the list of author names
# on line 25 and 27.

IFTTT_PATHS = [
                os.path.join(HOME, 'Dropbox', 'ifttt', 'instascriptogram'),
                os.path.join(HOME, 'Dropbox', 'ifttt', 'instascriptogram_steph')
            ]

# Your Scriptogr.am API Key
APP_KEY = ""
# Your Scriptogr.am User ID
USER_ID = ""  
# Change this if you don't want Pushover notifications for each post
# Don't forget to add your own token and user
NOTIFY_ME = False
# List of the possible authors. This should correlate with your IFTTT_PATHS
AUTHOR_NAMES = ['Ryan', 'Steph']
# Pick who the default author is if the folder names don't find an author.
DEFAULT_AUTHOR = "Ryan"

# Define the tag you used for your IFTTT recipe
WATCHED_TAG = "" 

# The content of your Scriptogr.am post. 
# Feel free to edit however you want.
# For an example post, visit
# http://keephouseadventures.com/post/instagram-pic-for-tuesday-sep-03
POST_TEXT = \
"""---
Date: %s
Title: Instagram Pic for %s
Type: post
Tags: instagram 
---

![](%s)  

%s

\-%s

"""


def pushover(title, message):
    import httplib, urllib
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
            urllib.urlencode({
                "token": "", # Pushover token
                "user": "", # Pushover user
                "title": title,
                "message": message,
      }),{ "Content-type": "application/x-www-form-urlencoded" })


def send_notification(name):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from pushover import pushover

    pushover(
        '(Insta|Scripto)gram',
        'A Instagram post was made by %s' % name
        )

def logged_files(pathname, filename):
    if not os.path.exists(os.path.join(pathname, 'logged')):
        os.mkdir(os.path.join(pathname, 'logged'))
    os.rename(
        os.path.join(pathname, filename),
        os.path.join(pathname, 'logged', filename)
        )


def post_to_blog(content, date):
    # Info found at https://github.com/khertan/KhtNotes/blob/master/khtnotes/scriptogram.py

    class NetworkError(Exception):
        pass
    
    datas = {
        'app_key': APP_KEY,
        'user_id': USER_ID,
        'name': 'instagram_%s' % created_at.strftime("%y%m%d%H%M%S"),
        'text': POST_CONTENT
    }
    
    url = 'http://scriptogr.am/api/article/post/'

    res = requests.post(url, data=datas)
    return res
    if res.status_code != requests.codes.ok:
        raise NetworkError('HTTP Error : %d' % res.status_code)
    else:
        if 'status' not in res.json():
            raise NetworkError('Invalid answer from scriptogr.am API'
                               % res.json()['reason'])
        if res.json()['status'] != 'success':
            raise NetworkError('%s' % res.json()['reason']) 

for IFTTT_PATH in IFTTT_PATHS:
    file_list = [f for f in os.listdir(IFTTT_PATH) if f.endswith('.txt')]
    
    # Keep going if there are no text files
    if not file_list:
        continue

    for text_file in file_list:
        f = open(os.path.join(IFTTT_PATH, text_file), 'r+')
        f = [line.replace('\n', '') for line in f.readlines()]

        source_url = f[0]
        instagram_url = f[1]
        caption = f[2]
        created_at = datetime.strptime(f[3], '%B %d, %Y at %I:%M%p')
        
        for author_name in AUTHOR_NAMES:
            if author_name.lower() in IFTTT_PATH.lower():
                name = author_name.title()
            else:
                name = DEFAULT_AUTHOR.title()

        # Skips the post if the watched tag isn't in the caption.
        if WATCHED_TAG and WATCHED_TAG not in caption:
            continue
        else:
            caption = caption.replace(WATCHED_TAG, '')

        POST_CONTENT = POST_TEXT % (
                                    created_at,
                                    created_at.strftime("%A, %b %d"),
                                    source_url,
                                    caption,
                                    name
                                    )
        post = post_to_blog(POST_CONTENT, created_at)

        # Move the text file into the logged folder.
        logged_files(IFTTT_PATH, text_file)
        
        if NOTIFY_ME:
            send_notification(name)

        # Scriptogr.am limits 1 API call per 10 seconds. Being nice to their API.
        sleep(10)
