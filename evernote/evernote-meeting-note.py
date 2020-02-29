# coding: utf-8

# https://gist.github.com/Moving-Electrons/7000517

# Evernote Template Note - Pythonista

# This script uses Evernote's API to create a new template note to be used in meetings.
# The template includes the following fields: Date, Time, Attendance, Objective, Remarks and
# Action Items. The fields are shown using Evernote Markup Language. It also automatically
# adds the the date when the note was created at the end of the note's title.
#
# When run, it lists all notebooks in a user's account (just as reference), then
# asks for the title of the new note (automatically adding the current date at the
# end in ISO format YYYY-MM-DD), then asks for the tags to be assigned to the note and
# creates it in a pre-defined notebook (hard coded in the ntbkName variable below).
#
# It was made using the sample script by Pythonista's creator Ole Zorn as a baseline. I modified it
# to suit my needs.
#
# Please, keep in mind Before running this sample, you must fill in your Evernote developer token!
#
# To get a developer token, visit
# https://www.evernote.com/api/DeveloperToken.action


#Constants
from __future__ import print_function
ntbkName = "Work"
auth_token = "INSERT YOUR EVERNOTE TOKEN HERE"

# This assumes that this script is in the root folder, and the Evernote SDK
# is installed in the 'evernote-sdk' directory, using this installer script:
# https://gist.github.com/5048588

import sys
sys.path.append('evernote-sdk')

import clipboard
import console
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
from datetime import date


dt = date.today()
todayDt = dt.isoformat()

print("Connecting to Evernote...\n")

client = EvernoteClient(token=auth_token, sandbox=False)
note_store = client.get_note_store()

# List all of the notebooks in the user's account
notebooks = note_store.listNotebooks()
print("Found ", len(notebooks), " notebooks:")

for notebook in notebooks:
	print("  * ", notebook.name)
	if notebook.name == ntbkName:
		print("<Target Notebook Found>")
		# gets the notebook GUID to assign it to the new Note
		ntbkGuid = notebook.guid
		
print("Creating a new note in notebook "+ntbkName)


# To create a new note, simply create a new Note object and fill in
# attributes such as the note's title.

note = Types.Note()

title = console.input_alert("Note's Title")
tags = ""
tags = console.input_alert("Note's Tags","separated by spaces")


note.title = title+' - '+todayDt
if tags != "":
	note.tagNames = tags.split()
note.notebookGuid = ntbkGuid

# The content of an Evernote note is represented using Evernote Markup
# Language (ENML). The full ENML specification can be found in the Evernote
# API Overview at
# http://dev.evernote.com/documentation/cloud/chapters/ENML.php

note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM ' \
   '"http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;">'
note.content += '<div><b>Date: </b>&nbsp;</div>'
note.content += '<div><b>Time: </b>&nbsp;<br/><br/></div>'
note.content += '<div><b>Attendance: </b></div><br/><br/>'
note.content += '<div><hr/><br/></div>'
note.content += '<div><b>Objective </b><br/><br/><br/></div>'
note.content += '<div><b>Remarks </b><br/><br/><br/></div>'
note.content += '<div><b>Action Items </b></div>'
note.content += '<div><ol><li><br/></li></ol></div>'
note.content += '</en-note>'


# Finally, send the new note to Evernote using the createNote method
# The new Note object that is returned will contain server-generated
# attributes such as the new note's unique GUID.

created_note = note_store.createNote(note)

print("Successfully created a new note with GUID: ", created_note.guid)

