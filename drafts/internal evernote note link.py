# http://blog.jeffreykishner.com/2014/07/01/getADirectLinkToAnyNoteInEvernoteForIos
# https://discussion.evernote.com/topic/39792-cant-create-note-links-in-en-ios-clients/
# coding: utf-8
import clipboard
import sys
import webbrowser
import console
import urllib

mytext = (sys.argv[1])
head, sep, tail = mytext.rpartition('/')
parttwo = head.replace('https://www.evernote.com/shard/s45/sh/', '')
evernoteurl = ('evernote:///view/4444444/s45/' + parttwo + '/' + parttwo + '/')

webbrowser.open('drafts4://x-callback-url/create?text=' + evernoteurl + '&action=Copy%20to%20Clipboard')
# pythonista://internal%20evernote%20note%20link?action=run&argv=[[draft]]