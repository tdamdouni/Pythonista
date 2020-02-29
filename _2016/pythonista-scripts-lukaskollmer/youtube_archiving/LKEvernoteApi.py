# coding: utf-8
from __future__ import print_function
import re
import sys
import console
import datetime
import clipboard
from string import Template
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import evernote.edam.userstore.constants as UserStoreConstants
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec


#__all__ = ['log_progress', 'get_all_notebooks', 'appentToNote']

log_progress = True


_auth_token = '__YOUR_EVERNOTE_AUTH_TOKEN_HERE__'
_progress = 0

_client = None
_note_store = None

def _get_client():
	global _client
	if _client is None:
		log_progress('login to evernote')
		_client = EvernoteClient(token=_auth_token, sandbox=False)
	return _client

def _get_note_store():
	global _note_store
	if _note_store is None:
		log_progress('load the note store')
		_note_store = _get_client().get_note_store()
	return _note_store


def log_progress(msg, color='default'):
	global log_progress
	global _progress
	if log_progress:
		progress_str = str(_progress).zfill(2)
		message = '{0} – {1}'.format(progress_str, msg)
		print(message)
		_progress += 1

def get_all_notebooks():
	return _get_note_store().listNotebooks()

def get_all_notes_in_notebook(notebook):
	guid = notebook.guid
	filter = NoteFilter(notebookGuid=guid)

	#def __init__(self, includeTitle=None, includeContentLength=None, includeCreated=None, includeUpdated=None, includeDeleted=None, includeUpdateSequenceNum=None, includeNotebookGuid=None, includeTagGuids=None, includeAttributes=None, includeLargestResourceMime=None, includeLargestResourceSize=None,):
	resultsSpec = NotesMetadataResultSpec(includeTitle=True)
	fetch_results = _get_note_store().findNotesMetadata(filter, 0, 10, resultsSpec)
	real_notes = []
	for n in fetch_results.notes:
		#note = _get_note_store().getNote(n.guid, withContent=True, withResourcesData=False, withResourcesRecognition=False, withResourcesAlternateData=False)
		note = _get_note_store().getNote(n.guid, True, False, False, False)
		real_notes.append(note)
	return real_notes

#Accepts the GUID(string) of the note you want to append
def append_to_note(guid, new_content, main_new_content, add_if_already_exists):

	#Get the note to be updated using the note's guid http://dev.evernote.com/documentation/reference/NoteStore.html#Fn_NoteStore_getNote
	note_store = _get_note_store()

	log_progress('load the \'2Archive\' note')
	note = note_store.getNote(guid, True, True, False, False)

	#Regular expressions used to replicate ENML tags.  These same tags will be used to "rebuild" the note with the existing note metadata
	log_progress('do the regEx stuff')
	xmlTag          = re.search('<\?xml.*?>', note.content).group()
	docTag          = re.search('<\!DOCTYPE.*?>', note.content).group()
	noteOpenTag     = re.search('<\s*en-note.*?>', note.content).group()
	noteCloseTag    = re.search('<\s*/en-note.*?>', note.content).group()
	breakTag        = '<br />'

	#Rebuild the note using the new content
	log_progress('Rebuild the note using the new content')
	content           =  note.content.replace(xmlTag, "").replace(noteOpenTag, "").replace(noteCloseTag, "").replace(docTag, "").strip()

	if main_new_content in content:
		if add_if_already_exists:
			content += breakTag + "".join(new_content)
		else:
			log_progress('url already in note')
	else:
		content += breakTag + ''.join(new_content)
	template          =  Template ('$xml $doc $openTag $body $closeTag')
	note.content      =  template.substitute(xml=xmlTag,doc=docTag,openTag=noteOpenTag,body=content,closeTag=noteCloseTag)

	#Update the note

	log_progress('save the updated note to evernote')
	try:
		_get_note_store().updateNote(note)
	except:
		print(sys.exc_info())

	#Return updated note (object) to the function
	return note

if __name__ == '__main__':
	pass
