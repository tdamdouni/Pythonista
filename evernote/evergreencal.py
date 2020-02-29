# https://gist.github.com/mcsquaredjr/0e92cc9531d8ec28c0f8

'''
EvergreenCal: process Evernote notes, create events, and
cross-reference notes with events.
'''
from __future__ import print_function

__author__ = 'Serge Boyko aka mcsquaredjr'
__version__ = '0.4'
__date__ = 'Tuesday, March 12th, 2013, 23:55:12'
__email__ = "nevergreencal@gmail.com"


# The MIT License
#
# Copyright (c) 2013 McSquaredJr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
# Try to determine if we are in Pythonista
try:
	# to import a Pythonista-specific module
	from scene import Layer
	in_pythonista = True
	del(sys.modules['scene'])
except ImportError:
	in_pythonista = False
	
if in_pythonista:
	sys.path.append('../')
	sys.path.append('../evernote-sdk')
	sys.path.append('../google-api')
	
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors
from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore

import gflags
import httplib2

from apiclient.discovery import build

from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

import os
import datetime
import time
import parsedatetime as pdt
import argparse


############################################################
#                CONSUMER KEYS AND SECRETS                 #
############################################################
# These are used to get your own tokens; you can't do anything
# with them.
EN_URL = 'https://www.evernote.com'
EN_CONSUMER_KEY = 'mcsquaredjr'
EN_CONSUMER_SECRET = '8aa0cc20a83960d6'
GC_CLIENT_ID = '566481039830.apps.googleusercontent.com'
GC_CLIENT_SECRET = 'cicukUfWZi4tQK1nb4OzU837'
GC_SCOPE = 'https://www.googleapis.com/auth/calendar'
GC_USER_AGENT = 'EvergreenCal'
GC_DEV_KEY = 'AIzaSyCRmYP_h_j8cQxkDeyWkp4o0ww14bItrLM'


############################################################
#                CLASS EVERNOTE_PROCESSOR                  #
############################################################
class Evernote_Processor(object):
	'''Represents objects and methods to access, update, and
	process Evernote notes and their attributes to extract due
	dates and link with Google Calendar Events.
	'''
	def __init__(self, consumer_key, consumer_secret):
		'''Create EN processor instance and EN client.'''
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.client = self.create_client()
		self.user_store = self.client.get_user_store()
		self.note_store = self.client.get_note_store()
		self.shard_id = self.get_shard_id()
		
		
	def parse_query_string(self, authorize_url):
		'''Helper function to turn query string parameters into a
		Python dictionary.
		'''
		uargs = authorize_url.split('?')
		vals = {}
		if len(uargs) == 1:
			raise Exception('Invalid authorization URL')
		for pair in uargs[1].split('&'):
			key, value = pair.split('=', 1)
			vals[key] = value
		return vals
		
		
	def create_client(self, storage_name='evernote.dat'):
		'''Create an instance of EN client and set auth_token.'''
		# Try check if storage file exists
		if os.path.isfile(storage_name) is True:
			# Try to read it
			try:
				storage = open(storage_name, 'r')
				auth_token = storage.read()
				# We will need it for some methods
				self.token = auth_token
				try:
					# NB: sandbox=False for production
					client = EvernoteClient(token=auth_token, sandbox=False)
					# Now try to get user_store if Exception is thrown fall
					# back to reauthorization
					user_store = client.get_user_store()
					user = user_store.getUser().username
				except Exception as e:
					print('Authorization error: ', e)
					print('Will need to re-authorize.')
					client = self.authorize(storage_name)
					
			except IOError as e:
				print('Error while reading the auth token: ', e)
				client = None
			finally:
				storage.close()
		else:
			# No storage found, we will need to authorize the app
			# to get the token
			client = self.authorize(storage_name)
		return client
		
	def authorize(self, storage_name):
		'''Authorize/reauthorize the app if something is wrong
		with the token or storage.
		'''
		# Start oauth flow
		client = EvernoteClient(
		consumer_key=self.consumer_key,
		consumer_secret=self.consumer_secret,
		sandbox=False)
		
		request_token = client.get_request_token('http://localhost')
		#Prompt the user to open the request URL in their browser
		print("Paste this URL in your browser and login\n")
		print(client.get_authorize_url(request_token) + '\n')
		# Have the user paste the resulting URL so we can pull it
		# apart
		print("Paste the URL after login here:")
		authurl = raw_input()
		## Parse the URL to get the OAuth verifier
		vals = self.parse_query_string(authurl)
		# Use the OAuth verifier and the values from request_token
		# to built the request for our authentication token, then
		# ask for it.
		auth_token = client.get_access_token(
		request_token['oauth_token'],
		request_token['oauth_token_secret'],
		vals['oauth_verifier'])
		# We will need it for some methods
		self.token = auth_token
		# Write it to the storage file
		try:
			storage = open(storage_name, 'w')
			storage.write(auth_token)
		except ImportError as e:
			# Should never happen
			print('Error while saving the auth token: ', e)
			print('Your auth token is: ', auth_token)
		finally:
			storage.close()
		# We will proceed anyway
		try:
			# NB: sandbox=False for production
			client = EvernoteClient(token=auth_token, sandbox=False)
		except Exception as e:
			print('Cannot create EN client: ', e)
			client = None
		return client
		
	def clear_storage(self, storage_name='evernote.dat'):
		'''Clear storage file on the client'''
		try:
			os.remove(storage_name)
		except OSError as e:
			print('Cannot delete storage file: ', e)
			
			
	def check_version(self):
		'''Check for version'''
		version_ok = self.user_store.checkVersion(
		"Version check",
		UserStoreConstants.EDAM_VERSION_MAJOR,
		UserStoreConstants.EDAM_VERSION_MINOR
		)
		if not version_ok:
			return -1
		else:
			return 0
			
			
	def _make_note(self, title, content, url):
		'''Prepare a note to be posted'''
		note = Types.Note()
		note.title = title
		# Set up note attributes
		attrs = Types.NoteAttributes()
		attrs.sourceURL = url
		note.attributes = attrs
		note.content = '<?xml version="1.0" encoding="UTF-8"?>'
		note.content += '<!DOCTYPE en-note SYSTEM ' \
		'"http://xml.evernote.com/pub/enml2.dtd">'
		# Wrap content in <en-note>
		note.content += '<en-note>'
		note.content += content
		note.content += '</en-note>'
		return note
		
		
	def get_shard_id(self):
		'''
		Get the User from user_store and return the user's shard ID
		'''
		try:
			user = self.user_store.getUser(self.token)
		except (Errors.EDAMUserException,
		Errors.EDAMSystemException) as e:
			print("Exception while getting user's shardID:")
			print(type(e), e)
			return None
			
		if hasattr(user, 'shardId'):
			return user.shardId
		return None
		
		
	def post_note(self, title, note, url):
		'''Post a note to Evernote'''
		ver = self.check_version()
		if ver < 0:
			print('*** VERSION ERROR: Update client to the latest version.')
		else:
			note = self._make_note(title, note, url)
			try:
				created_note = self.note_store.createNote(note)
				
			except (Errors.EDAMUserException,
			Errors.EDAMSystemException) as e:
				print("Exception while getting user's shardID:")
				print(type(e), e)
				return None
				
			if hasattr(created_note, 'guid'):
				return created_note.guid
			return None
			
			
	def get_notebook_guid(self, notebook_name):
		'''Return notebooks guid given the notebook name'''
		if notebook_name is not None:
			notebooks = self.note_store.listNotebooks()
			# Iterate over notebooks until a given mame is not found
			# Return None if non-existing name is given
			matched_notebook = next((notebook for notebook in notebooks \
			if notebook.name == notebook_name), None)
			if matched_notebook is not None:
				guid = matched_notebook.guid
			else:
				guid = None
				print('*** Warning: notebook {0} was not found.'.format(notebook_name))
		else:
			guid = self.note_store.getDefaultNotebook().guid
		return guid
		
		
	def get_notes(self, notebook_name, words=None, offset=0, max_num=25):
		'''Get max_num notes from a notebook'''
		# This is how we construct a filter, we cannot get it from
		# an instance of the NoteStore
		filter = NoteStore.NoteFilter()
		# Evernote search grammar is described here:
		# http://dev.evernote.com/documentation/cloud/chapters/search_grammar.php
		guid = self.get_notebook_guid(notebook_name)
		if guid is not None:
			filter.notebookGuid = guid
			if words is not None:
				# words is an attribute in Python
				filter.words = words
			try:
				notes_list = self.note_store.findNotes(self.token,
				filter,
				0,
				max_num)
			except Exception as e:
				print('Exception while finding notes: ', e)
				notes_list = None
		else:
			notes_list = None
		# NoteList is not a Python list, but a structure
		return notes_list
		
		
	def get_note_url(self, guid):
		'''
		Share a single note and return the public URL for the note
		'''
		if not self.shard_id:
			self.shard_id = self.get_shard_id()
			if not self.shard_id:
				raise SystemExit
		try:
			share_key = self.note_store.shareNote(self.token, guid)
		except (EDAMNotFoundException,
		EDAMSystemException,
		EDAMUserException) as e:
			print("Error sharing note:")
			print(type(e), e)
			return None
		return "%s/shard/%s/sh/%s/%s" % \
		(EN_URL, self.shard_id, guid, share_key)
		
		
	def get_note_due_date(self, note):
		'''Extract due date from a note title'''
		title = note.title
		ind = title.find('__')
		ddate = title[ind+2:]
		# Rerurn note's title (without due date) and due date
		return (title[:ind].strip(), ddate.strip())
		
		
	def update_note(self, note, new_title, url):
		'''Update note title for processed notes'''
		note.title = new_title
		attrs = Types.NoteAttributes()
		attrs.sourceURL = url
		note.attributes = attrs
		# Update the note with new_title
		try:
			updated_note = self.note_store.updateNote(note)
			return updated_note.guid
		except Exception as e:
			print('Exception while updating note: ', e)
			return None
			
			
############################################################
#                     CLASS GCAL_EVENT                     #
############################################################
class GCal_Event(object):
	'''Access and create events in Google Calendar and link with
	Evernote notes representing actions with due dates.'''
	def __init__(self):
		FLAGS = gflags.FLAGS
		FLOW = OAuth2WebServerFlow(
		client_id=GC_CLIENT_ID,
		client_secret=GC_CLIENT_SECRET,
		scope=GC_SCOPE,
		user_agent=GC_USER_AGENT)
		# We need to disable it for an installed app
		FLAGS.auth_local_webserver = False
		# Read credentials if available
		storage = Storage('calendar.dat')
		credentials = storage.get()
		if credentials is None or credentials.invalid == True:
			credentials = run(FLOW, storage)
		# Create an httplib2.Http object to handle our HTTP requests
		# and authorize it with our good Credentials.
		http = httplib2.Http()
		http = credentials.authorize(http)
		# Build a service object for interacting with the API
		self.service = build(serviceName='calendar',
		version='v3',
		http=http,
		developerKey=GC_DEV_KEY)
		
		
	def get_service(self):
		'''Get service object'''
		return self.service
		
		
	def generate_event(self, start, end, tz, location, summary, desc):
		'''Generate event from provided data'''
		start_dict = dict()
		start_dict['dateTime'] = start
		start_dict['timeZone'] = tz
		end_dict = dict()
		end_dict['dateTime'] = end
		end_dict['timeZone'] = tz
		evt_dict = dict()
		evt_dict['kind'] = 'calendar#event'
		evt_dict['status'] = 'confirmed'
		evt_dict['summary'] = summary
		evt_dict['description'] = desc
		evt_dict['summary'] = summary
		evt_dict['start'] = start_dict
		evt_dict['end'] = end_dict
		evt_dict['location'] = location
		evt_dict['colorId'] = '2' # Mint!
		return evt_dict
		
		
	def create_event(self, cal_id, evt):
		'''Create event in Google calendar, identified by cal_id'''
		try:
			events = self.get_service().events()
			created_evt = events.insert(body=evt,
			calendarId=cal_id).execute()
			return created_evt['htmlLink']
		except Exception as e:
			print('Exception while creating event: ', e)
			return None
			
			
############################################################
#                   CLASS GREEN_CALENDAR                   #
############################################################
class Green_Calendar(object):
	'''Controller class'''
	
	def __init__(self):
		self.ep = Evernote_Processor(EN_CONSUMER_KEY, EN_CONSUMER_SECRET)
		self.gc = GCal_Event()
		self.start_time = time.time()
		
		
	def process_due_date(self, due_date_str, duration=15):
		'''Parse date string and return start date/time in format used
		by Google Calendar (RFC-3889).
		'''
		c = pdt.Constants()
		c.BirthdayEpoch = 80
		p = pdt.Calendar(c)
		result = p.parse(due_date_str)
		# Unpack the tuple and convert to string
		start = datetime.datetime(*result[0][0:6])
		end = start + datetime.timedelta(minutes=duration)
		# Ignore seconds
		start_str = start.strftime('%Y-%m-%dT%H:%M:00')
		end_str = end.strftime('%Y-%m-%dT%H:%M:00')
		return (start_str, end_str, result[1])
		
		
	def _setup(self,
	notebooks,      # list of notebooks, use default if None
	sep,            # separator before due date
	sep_proc,       # separator in processed notes
	max_age,        # seach notes not older than max_age
	cal_id          # Google calendar ID
	):
		'''Configure EvergreenCal'''
		self.notebooks = notebooks
		self.sep = sep
		self.sep_proc = sep_proc
		self.max_age = max_age
		self.cal_id = cal_id
		
		
	def run(self, forget=None):
		'''Glue all pieces together, parse dates, cross-link notes
		and events.
		'''
		if forget is not None:
			self.ep.clear_storage(forget)
			sys.exit(0)
			
		# Configure search
		words = 'intitle:"{0}"'.format(self.sep)
		# Find all matching notes
		notes_list = []
		if self.notebooks is None:
			notes = self.ep.get_notes(None,
			words=words,
			offset=0,
			max_num=25)
			notes_list.append(notes.notes)
		else:
			if type(self.notebooks) is list:
				for notebook in self.notebooks:
					#print notebook
					notes = self.ep.get_notes(notebook,
					words=words,
					offset=0,
					max_num=25)
					if notes is not None:
						notes_list.append(notes.notes)
			else:
				raise TypeError('Notebooks must be a list or a None-type.')
		# Flatten the note list
		notes_list = [item for sublist in notes_list for item in sublist]
		fmt ='{:<5}{:<24}{:<45}{:<5}'.format('No.', 'Due date/time', 'Note title', 'Result')
		print('\nPROCESSING REPORT')
		print('-'*len(fmt))
		print(fmt)
		print('-'*len(fmt))
		# Start processing here
		for i, note in enumerate(notes_list):
			title, ddate = self.ep.get_note_due_date(note)
			(start, end, result) = self.process_due_date(ddate)
			if result > 0:
				note_url = self.ep.get_note_url(note.guid)
				# Create time zone string
				# TODO: take into account periods when Europe ans USA are
				# not in sync when switching to the summer/winter time
				tz = str.format('{0:+06.2f}', float(-time.timezone)/3600)
				tz = 'UTC' + tz
				location = 'Evernote'
				description = note_url + '\n\n--Created by EvergreenCal'
				evt = self.gc.generate_event(start,
				end,
				tz,
				location,
				title,
				description)
				# Construct new title
				title = title + ' ' + self.sep_proc + ' ' + start
				# Create event and update the note
				evt_url = self.gc.create_event(self.cal_id, evt)
				guid = self.ep.update_note(note, title, evt_url)
				if (guid is not None) and (evt_url is not None):
					result = 'OK'
				else:
					result = 'Error'
				# Truncate the title for report
				title_ = (title[:40] + '...') if len(title) > 40 else title
				fmt ='{:<5}{:<24}{:<45}{:^4}'.format(i+1,
				start,
				title_,
				result)
				print(fmt)
			else:
				# We cannot parse the date; no events created
				result = 'Error'
				title_ = (title[:40] + '...') if len(title) > 40 else title
				fmt ='{:<5}{:<24}{:<45}{:<5}'.format(i+1,
				'UNDEFINED',
				title_,
				result)
				print(fmt)
		print('-'*len(fmt))
		e_time = time.time() - self.start_time
		print('Elapsed time: {0:f}'.format(e_time))
		print('The number of processed notes is: {0:d}'.format(len(notes_list)))
		
		
if __name__ == '__main__':
	# Change the values below if you want different defaults
	# You do not need to supply a value for notebooks if you want
	# to use the default notebook
	defaults = dict()
	defaults['max_age'] = 7
	defaults['sep'] = '__'
	defaults['sep_proc'] = '##'
	defaults['cal_id'] = 'primary'
	defaults['storage'] = None
	# Create a parser
	parser = argparse.ArgumentParser(description='parse evernote notes, \
	create events in google calendar, and \
	cross-reference notes and events',
	usage='python evergreencal.py -h',
	prog='EvergreenCal',
	epilog='report bugs to nevergreencal@gmail.com.')
	parser.add_argument('--notebooks', '-n',
	help='whitepace-delimited list of notebooks to \
	search within',
	nargs='+',
	type=str,
	metavar='LIST'
	)
	parser.add_argument('--max_age', '-a',
	help='do not process notes older than M days',
	type=int,
	metavar='M',
	default=defaults['max_age']
	)
	parser.add_argument('--sep', '-s',
	help='separator used for non-processed notes \
	(default is "__")',
	type=str,
	metavar='S',
	default=defaults['sep']
	)
	parser.add_argument('--sep_proc', '-p',
	help='separator used for proceesed notes \
	(default is "##")',
	type=str,
	metavar='P',
	default=defaults['sep_proc']
	)
	parser.add_argument('--cal_id', '-c',
	help='id of the calendar used for created events',
	type=str,
	metavar='ID',
	default=defaults['cal_id']
	)
	parser.add_argument('--forget', '-f',
	help='forget authorization stored in \
	FILE and re-authorize',
	type=str,
	metavar='FILE',
	default=defaults['storage']
	)
	args = parser.parse_args()
	# Now run!
	gc = Green_Calendar()
	gc._setup(notebooks=args.notebooks,
	sep=args.sep,
	sep_proc=args.sep_proc,
	max_age=args.max_age,
	cal_id=args.cal_id)
	gc.run(forget=args.forget)

