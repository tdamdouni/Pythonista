# A simple Evernote API demo script that lists all notebooks in the user's
# account and creates a simple test note in the default notebook.
#
# Before running this sample, you must fill in your Evernote developer token!
# 
# This sample is part of the Evernote SDK and has been modified slightly for
# Pythonista, to take advantage of the clipboard and PIL modules.
# If there is an image in the clipboard when the script is run, it is attached
# to the sample note.

# Real applications authenticate with Evernote using OAuth, but for the
# purpose of exploring the API, you can get a developer token that allows
# you to access your own Evernote account.

# To get a developer token, visit
# https://www.evernote.com/api/DeveloperToken.action

auth_token = "YOUR_DEVELOPER_TOKEN"

# This assumes that this script is in the root folder, and the Evernote SDK
# is installed in the 'evernote-sdk' directory, using this installer script:
# https://gist.github.com/5048588

import sys
sys.path.append('evernote-sdk')

import clipboard
from io import BytesIO

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient

client = EvernoteClient(token=auth_token, sandbox=False)
note_store = client.get_note_store()

# List all of the notebooks in the user's account
notebooks = note_store.listNotebooks()
print "Found ", len(notebooks), " notebooks:"
for notebook in notebooks:
    print "  * ", notebook.name
print "Creating a new note in the default notebook"

# To create a new note, simply create a new Note object and fill in
# attributes such as the note's title.
note = Types.Note()
note.title = "Test note from Pythonista"

# To include an attachment such as an image in a note, first create a Resource
# for the attachment. At a minimum, the Resource contains the binary attachment
# data, an MD5 hash of the binary data, and the attachment MIME type.
# It can also include attributes such as filename and location.
img = clipboard.get_image()
if img is not None:
	print 'Attaching image in clipboard...'
	buffer = BytesIO()
	img.save(buffer, 'png')
	image_data = buffer.getvalue()
	md5 = hashlib.md5()
	md5.update(image_data)
	hash = md5.digest()
	data = Types.Data()
	data.size = len(image_data)
	data.bodyHash = hash
	data.body = image_data
	resource = Types.Resource()
	resource.mime = 'image/png'
	resource.data = data
	# Now, add the new Resource to the note's list of resources
	note.resources = [resource]
	# To display the Resource as part of the note's content, include an
	# <en-media> tag in the note's ENML content. The en-media tag identifies
	# the corresponding resource using the MD5 hash.
	hash_hex = binascii.hexlify(hash)
	# The content of an Evernote note is represented using Evernote Markup
	# Language (ENML). The full ENML specification can be found in the Evernote
	# API Overview at
	# http://dev.evernote.com/documentation/cloud/chapters/ENML.php
	note.content = '<?xml version="1.0" encoding="UTF-8"?>'
	note.content += '<!DOCTYPE en-note SYSTEM ' \
    '"http://xml.evernote.com/pub/enml2.dtd">'
	note.content += '<en-note>Here is the attached image:<br/>'
	note.content += '<en-media type="image/png" hash="' + hash_hex + '"/>'
	note.content += '</en-note>'

# Finally, send the new note to Evernote using the createNote method
# The new Note object that is returned will contain server-generated
# attributes such as the new note's unique GUID.
created_note = note_store.createNote(note)

print "Successfully created a new note with GUID: ", created_note.guid

