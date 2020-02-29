from __future__ import print_function
# Uploads a text note to Evernote and shares it. Supports Markdown conversion to HTML.
# Link is printed to open in Chrome and stored in system clipboard
# Text is entered via input alert or third-party launcher
# From Drafts: pythonista://EvernoteTextShare?action=run&argv=[[title]]&argv=[[body]]
# Token is stored in Keychain, note is saved in default notebook
# Based on Brett Kelly's Python code: https://gist.github.com/inkedmn/4074431
# and Ole Zorn's demo scripts: http://omz-software.com/pythonista/forums/discussion/203/using-the-evernote-sdk-in-pythonista
# Requires Evernote dev token: https://www.evernote.com/api/DeveloperToken.action

import keychain
import clipboard
import console
import sys

sys.path.append('evernote-sdk')

# import token stored in Pythonista's keychain
auth_token = keychain.get_password('evernote','USERNAME')

# Construct URL. Replace "googlechromes://" with "safari-https://" if you want to open the note in Safari 
EN_HOST = "www.evernote.com"
EN_URL = "googlechromes://%s" % EN_HOST

console.clear()
numArgs = len(sys.argv)

# Count arguments, if less than 3 enter title and text manually. Use with apps like Drafts
# and Launch Center Pro
if numArgs < 3:
	title = console.input_alert('Note Title', 'Enter the title of your note')
	body = console.input_alert('Note Text', 'Enter the text of your note')
else:
	print("Text received from another app, processing...")
	title = sys.argv[1]
	body = sys.argv[2]

console.show_activity()

# Convert Markdown text to valid HTML
# Add or remove extras to your liking
from markdown2 import markdown
text = markdown(body, extras=['footnotes', 'header-ids'])

print("Generating note...")
 
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
 
client = EvernoteClient(token=auth_token, sandbox=False)
note_store = client.get_note_store()
userStore = client.get_user_store()

note = Types.Note()
note.title = title

# Generate note content and upload
# The content of an Evernote note is represented using Evernote Markup
# Language (ENML). The full ENML specification can be found in the Evernote
# API Overview at
# http://dev.evernote.com/documentation/cloud/chapters/ENML.php
	
note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM ' \
    '"http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>'
note.content += text
note.content += '</en-note>'
note.content = note.content.encode('utf-8') # assign the result to change original string
	
print("Uploading clip to Evernote...")
created_note = note_store.createNote(note)
noteGuid = created_note.guid

#Get user shardID and the note's unique share key
user = userStore.getUser(auth_token).shardId
shareKey = note_store.shareNote(auth_token, noteGuid)
console.hide_activity()

print("Note URL set to clipboard. The note has been shared with the following URL:\n\n", end=' ') 
# Last, create two separate URLs for the browser you want to use
# and the link you want to share in the clipboard
final = "%s/shard/%s/sh/%s/%s" % \
		(EN_URL, user, noteGuid, shareKey)
		
shareable = "%s/shard/%s/sh/%s/%s" % \
		("https://www.evernote.com", user, noteGuid, shareKey)		
		
console.write_link(shareable, final)
clipboard.set(shareable)
