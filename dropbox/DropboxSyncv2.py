# https://gist.github.com/KainokiKaede/015601fc9f29c354a805fc56deef1bbe

# https://forum.omz-software.com/topic/3221/request-token-not-found-from-dropbox-sync-in-pythonista-3/2

from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import pickle
import console
import editor
import dropbox

# I moved 'dropboxlogin' into a sub folder so it doesn't clutter my main folder
sys.path += [os.path.join(os.path.dirname(os.path.abspath(__file__)),)]
import dropboxloginv2 # this code can be found here https://gist.github.com/4034526

STATE_FILE = '.dropbox_state_v2'

class dropbox_state:
	def __init__(self):
		self.cursor = None
		self.local_files = {}
		self.remote_files = {}

	# use ignore_path to prevent download of recently uploaded files
	def execute_delta(self, client, ignore_path = None):
		if not self.cursor:
			delta = client.files_list_folder('', recursive=True)
		else:
			delta = client.files_list_folder_continue(self.cursor)
		self.cursor = delta.cursor

		for entry in delta.entries:
			path = entry.path_display[1:]
			meta = entry

			# this skips the path if we just uploaded it
			if path != ignore_path:
				if meta != None:
					path = meta.path_display[1:] # caps sensitive
					if type(meta) == dropbox.files.FolderMetadata:
						print('\n\tMaking Directory:',path)
						self.makedir_local(path)
					elif path not in self.remote_files:
						print('\n\tNot in local')
						self.download(client, path)
					elif meta.rev != self.remote_files[path].rev:
						print('\n\tOutdated revision')
						self.download(client, path)
				# remove file or directory
				else:
					if os.path.isdir(path):
						print('\n\tRemoving Directory:', path)
						os.removedirs(path)
					elif os.path.isfile(path):
						print('\n\tRemoving File:', path)
						os.remove(path)
						del self.local_files[path]
						del self.remote_files[path]
					else:
						pass # file already doesn't exist localy

	# makes dirs if necessary, downloads, and adds to local state data
	def download(self, client, path):
		print('\tDownloading:', path)
		head, tail = os.path.split(path)
		if not os.path.exists(head) and head != '':
			os.makedirs(head)
		meta = client.files_download_to_file(path, os.path.join('/',path))
		self.local_files[path] = {'modified': os.path.getmtime(path)}
		self.remote_files[path] = meta

	def upload(self, client, path):
		print('\tUploading:', path)
		with open(path,'rb') as local:
			overwrite = dropbox.files.WriteMode('overwrite')
			meta = client.files_upload(local, os.path.join('/',path), overwrite)
			# meta = client.put_file(os.path.join('/',path), local, True)

		self.local_files[path] = {'modified': os.path.getmtime(path)}
		self.remote_files[path] = meta

		# clean out the delta for the file upload
		self.execute_delta(client, ignore_path=meta.path_display[1:])

	def delete(self, client, path):
		print('\tFile deleted locally. Deleting on Dropbox:',path)
		try:
			client.files_delete('/' + path)
		except Exception as e:
			# file was probably already deleted
			print(e)
			print('\tFile already removed from Dropbox')

		del self.local_files[path]
		del self.remote_files[path]

	# safely makes local dir
	def makedir_local(self,path):
		if not os.path.exists(path): # no need to make a dir that exists
			os.makedirs(path)
		elif os.path.isfile(path): # if there is a file there ditch it
			os.remove(path)
			del self.files[path]
			os.makedir(path)

	# recursively list files on dropbox
	def _listfiles(self, client, path = ''):
		meta = client.files_list_folder(path, recursive=True)
		filelist = []
		filelist += meta.entries
		while meta.has_more:
			meta = client.files_list_folder_continue(meta.cursor)
			filelist += meta.entries

		filelist = [i for i in filelist if type(i) == dropbox.files.FileMetadata]
		return filelist

	def download_all(self, client, path = '/'):
		filelist = self._listfiles(client)
		for file in filelist:
			self.download(client, file.path_display[1:])	# trim root slash

	def check_state(self, client, path):
		# lets see if we've seen it before
		if path not in self.local_files:
			# upload it!
			self.upload(client, path)
		elif os.path.getmtime(path) > self.local_files[path]['modified']:
			# newer file than last sync
			self.upload(client, path)
		else:
			pass # looks like everything is good

def loadstate():
	fyle = open(STATE_FILE,'rb')
	state = pickle.load(fyle)
	fyle.close()

	return state

def savestate(state):
	fyle = open(STATE_FILE,'wb')
	pickle.dump(state,fyle)
	fyle.close()

if __name__ == '__main__':
	console.show_activity()

	print("""
****************************************
*     Dropbox File Syncronization      *
****************************************""")

	client = dropboxlogin3v2.get_client()
	print('\nLoading local state')
	# lets see if we can unpickle
	try:
		state = loadstate()
	except:
		print('\nCannot find state file. ***Making new local state***')
		# Aaaah, we have nothing, probably first run
		state = dropbox_state()

		print('\nDownloading everything from Dropbox')
		# no way to check what we have locally is newer, gratuitous dl
		state.download_all(client)

	print('\nUpdating state from Dropbox')
	state.execute_delta(client)

	print('\nChecking for new or updated local files')
	# back to business, lets see if there is anything new or changed localy
	filelist = []
	for root, dirnames, filenames in os.walk('.'):
		for filename in filenames:
			if filename != STATE_FILE:
				filelist.append( os.path.join(root, filename)[2:])

	for file in filelist:
		state.check_state(client,file)

	print('\nChecking for deleted local files')
	old_list = list(state.local_files.keys())
	for file in old_list:
		if file not in filelist:
			state.delete(client, file)

	print('\nSaving local state')
	savestate(state)

	print('\nSync complete')
	console.hide_activity()

	print('\nReload file')
	if editor.get_path():
		editor.open_file(editor.get_path())
