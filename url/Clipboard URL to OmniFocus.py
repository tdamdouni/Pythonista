from __future__ import print_function
# https://gist.github.com/bachya/5c806bb14b9dd8a78268

# Script to scrape an HTML page's title and, along with its URL, send it to OmniFocus as a task.
# Author: Aaron Bach
# www: http://www.bachyaproductions.com/

import clipboard
import re
import sys
import urllib
import urllib2
import webbrowser

# Retrieve the input text from the clipboard:
cb_text = clipboard.get()

# Some apps (such as Overcast) don't just grab the URL when using
# the "Copy" share sheet action; sometimes, other text (such as a
# podcast title) is included. If this happens, I use that text
# (rather than going through the procedure of trying to grab the
# title from the HTML itself).

# Special thanks to John Gruber for the succinct, precise method
# for grabbing URLs out of a string.
GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
url = [ mgroups[0] for mgroups in GRUBER_URLINTEXT_PAT.findall(cb_text) ][0]

# Here, we deduce whether we need to get the URL title from the
# HTML itself, or if any extra info that came into the clipboard
# can be used.
if cb_text == url:
    try:
        # Collect the URL's title via its
        # page contents:
        req = urllib2.Request(url)

        # Some websites don't like bots grabbing their content;
        # get around this by using a fake user agent:
        req.add_header('User-Agent', 'Magic Browser')

        page = urllib2.urlopen(req)
        content = page.read()
        title = re.search('<title>(.*)</title>', content).group(1)
    except urllib2.HTTPError as e:
        # Something went wrong with the request, so just use
        # the URL itself as the title:
        title = url
else:
    # Use the extra information to get the title.
    title = cb_text.replace(url, '').strip()

# URL-encode the page's title and URL:
task_title = urllib.quote(sys.argv[1]) + ':%20' + urllib.quote(title)
task_note = urllib.quote(url)

if sys.argv[2] == 'Mail Drop':
    # If the user selects "Mail Drop",
    # create a note in Drafts and
    # trigger the "Email to OmniFocus"
    # action.
    draft = task_title + '%0A' + task_note

    drafts_url = ('drafts://x-callback-url/create?text='
                 + draft + '&action=Email%20to%20OmniFocus'
                 '&x-success=launch:&x-error=launch:&x-cancel=launch:')
    webbrowser.open(drafts_url)
elif sys.argv[2] == 'OmniFocus iOS':
    # If the user selects "OmniFocus iOS",
    # create a task directly in OmniFocus
    # using its URL scheme.
    webbrowser.open('omnifocus:///add?name=' + task_title + '&note=' + task_note)
else:
    print('Unknown task entry method: ' + sys.argv[2])