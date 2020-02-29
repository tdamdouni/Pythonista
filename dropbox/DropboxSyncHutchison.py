from __future__ import print_function
# Script to sync Pythonista files to Dropbox
# Author: David Hutchison
# www: http://www.devwithimagination.com/
import webbrowser, os, pprint
import dropbox
import hashlib
import json
import difflib
import sys

# Configuration
TOKEN_FILENAME = 'DBToken'
# Get your app key and secret from the Dropbox developer website
APP_KEY = ''
APP_SECRET = ''

# ACCESS_TYPE can be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'dropbox'

# Program, do not edit from here
VERBOSE_LOGGING = False

PYTHONISTA_DOC_DIR = os.path.expanduser('~/Documents')
SYNC_STATE_FOLDER = os.path.join(PYTHONISTA_DOC_DIR, 'dropbox_sync')
TOKEN_FILEPATH = os.path.join(SYNC_STATE_FOLDER, TOKEN_FILENAME)

pp = pprint.PrettyPrinter(indent=4)

# Method to get the MD5 Hash of the file with the supplied file name.
def getHash(file_name):
	# Open,close, read file and calculate MD5 on its contents 
	with open(file_name) as file_to_check:
		# read contents of the file
		data = file_to_check.read()    
		# pipe contents of the file through
		file_hash = hashlib.md5(data).hexdigest()
	return file_hash

# Method to configure the supplied dropbox session.
# This will use cached OAUTH credentials if they have been stored, otherwise the 
# user will be put through the Dropbox authentication process.
def configure_token(dropbox_session):
	if os.path.exists(TOKEN_FILEPATH):
		token_file = open(TOKEN_FILEPATH)
		token_key, token_secret = token_file.read().split('|')
		token_file.close()
		dropbox_session.set_token(token_key,token_secret)
	else:
		setup_new_auth_token(dropbox_session)
	pass

# Method to set up a new Dropbox OAUTH token.
# This will take the user through the required steps to authenticate.
def setup_new_auth_token(sess):
	request_token = sess.obtain_request_token()
	url = sess.build_authorize_url(request_token)
	
	# Make the user sign in and authorize this token
	print("url:", url)
	print("Please visit this website and press the 'Allow' button, then hit 'Enter' here.")
	webbrowser.open(url)
	raw_input()
	# This will fail if the user didn't visit the above URL and hit 'Allow'
	access_token = sess.obtain_access_token(request_token)
	#save token file
	token_file = open(TOKEN_FILEPATH,'w')
	token_file.write("%s|%s" % (access_token.key,access_token.secret) )
	token_file.close()
	pass
	
def upload(file, details, client, parent_revision):
	print("Trying to upload %s" % file)
	details['md5hash'] = getHash(file)
	print("New MD5 hash: %s" % details['md5hash'])

	response = client.put_file(file, open(file, 'r'), False, parent_revision)
	#print "Response: %s" % response
	details = update_file_details(details, response)
	
	print("File %s uploaded to Dropbox" % file)
	
	return details
	
def download(dest_path, dropbox_metadata, details, client):
	out = open(dest_path, 'w')
	file_content = client.get_file(dropbox_metadata['path']).read()
	out.write(file_content)
				
	details['md5hash'] = getHash(dest_path)
	print("New MD5 hash: %s" % details['md5hash'])
	details = update_file_details(details, dropbox_metadata)
	
	return details
	
def process_folder(client, dropbox_dir, file_details):
	
	# Get the metadata for the directory being processed (dropbox_dir).
	# If the directory does not exist on Dropbox it will be created.
	try:
		folder_metadata = client.metadata(dropbox_dir)
		
		if VERBOSE_LOGGING == True:
			print("metadata")
			pp.pprint(folder_metadata)
	except dropbox.rest.ErrorResponse as error:
		pp.pprint(error.status)
		if error.status == 404:
			client.file_create_folder(dropbox_dir)
			folder_metadata = client.metadata(dropbox_dir)
		else:
			pp.pprint(error)
			raise error
	
	# If the directory does not exist locally, create it.
	local_folder = os.path.join(PYTHONISTA_DOC_DIR, dropbox_dir[1:])
	if not os.path.exists(local_folder):
		os.mkdir(local_folder)
		

	# All the files that have been processed so far in this folder.
	processed_files = []
	# All the directories that exist on Dropbox in the current folder that need to be processed.
	dropbox_dirs = []
	# All the local directories in this current folder that do not exist in Dropbox.
	local_dirs = []
	
	# Go through the files currently in Dropbox and compare with local
	for file in folder_metadata['contents']:
		dropbox_path = file['path'][1:]
		file_name = file['path'].split('/')[-1]
		if file['is_dir'] == False and file['mime_type'].endswith('python'):
			
			if not os.path.exists(os.path.join(PYTHONISTA_DOC_DIR, dropbox_path)):
				print("Processing Dropbox file %s (%s)" % (file['path'], dropbox_path))
				try:
					
					
					if dropbox_path in file_details:
						# in cache but file no longer locally exists
						details = file_details[dropbox_path]
					
						print("File %s is in the sync cache and on Dropbox, but no longer exists locally. [Delete From Dropbox (del)|Download File (d)] (Default Delete)" % file['path'])
					
						choice = raw_input()
						if (choice == 'd'):
							download_file = True
						else: 
							# Default is 'del'
							download_file = False	
						
							#delete the dropbox copy
							client.file_delete(file['path'])
							file_details.remove(dropbox_path)
						
					else:
						details = {}
						download_file = True
					
					if (download_file ==  True):
						print("Downloading file %s (%s)" % (file['path'], dropbox_path))
						if VERBOSE_LOGGING == True:
							print(details)
					
						details = download(dropbox_path, file, details, client)
						file_details[dropbox_path] = details
				
					# dealt with this file, don't want to touch it again later
					processed_files.append(file_name)
					write_sync_state(file_details)
					
				except:
					pass
			else:
				# need to check if we should update this file
				# is this file in our map?
				if dropbox_path in file_details:
					details = file_details[dropbox_path]
					
					if VERBOSE_LOGGING == True:
						print("Held details are: %s" % details)
					
					if details['revision'] == file['revision']:
						# same revision
						current_hash = getHash(dropbox_path)
						
						if VERBOSE_LOGGING == True:
							print('New hash: %s, Old hash: %s' % (current_hash, details['md5hash']))
						
						if current_hash == details['md5hash']:
							print('File "%s" not changed.' % dropbox_path)
						else:
							print('File "%s" updated locally, uploading...' % dropbox_path)
							
							details = upload(dropbox_path, details, client, file['rev'])
							file_details[dropbox_path] = details
							
						processed_files.append(file_name)
					else:
						#different revision
						print('Revision of "%s" changed from %s to %s. ' % (dropbox_path, details['revision'], file['revision']))
						
						current_hash = getHash(dropbox_path)
						
						if VERBOSE_LOGGING == True:
							print('File %s. New hash: %s, Old hash: %s' % (dropbox_path, current_hash, details['md5hash']))
						
						if current_hash == details['md5hash']:
							print('File "%s" updated remotely. Downloading...' % dropbox_path)
							
							details = download(dropbox_path, file, details, client)
							file_details[dropbox_path] = details
						else:
							print("File %s has been updated both locally and on Dropbox. Overwrite [Dropbox Copy (d)|Local Copy (l)| Skip(n)] (Default Skip)" % file['path'])
							choice = raw_input()
				
							if choice == 'd' or choice == 'D':
								print("Overwriting Dropbox Copy of %s" % file)
								details = upload(dropbox_path, details, client, file['rev'])
								file_details[dropbox_path] = details
							elif choice == 'l' or choice == 'L':
								print("Overwriting Local Copy of %s" % file)
								details = download(dropbox_path, file, details, client)
								file_details[dropbox_path] = details
					
							
				else:
					# Not in cache, but exists on dropbox and local, need to prompt user
				
					print("File %s is not in the sync cache but exists both locally and on dropbox. Overwrite [Dropbox Copy (d)|Local Copy (l) | Skip(n)] (Default Skip)" % file['path'])
					choice = raw_input()
				
					details = {}
					if choice == 'd' or choice == 'D':
						print("Overwriting Dropbox Copy of %s" % file)
						details = upload(dropbox_path, details, client, file['rev'])
						file_details[dropbox_path] = details
					elif choice == 'l' or choice == 'L':
						print("Overwriting Local Copy of %s" % file)
						details = download(dropbox_path, file, details, client)
						file_details[dropbox_path] = details
					else:
						print("Skipping processing for file %s" % file)
				
				# Finished dealing with this file, update the sync state and mark this file as processed.	
				write_sync_state(file_details)
				processed_files.append(file_name)
		elif file['is_dir'] == True:
			dropbox_dirs.append(file['path'])
					

	# go through the files that are local but not on Dropbox, upload these.
	files = os.listdir(local_folder)
	for file in files:
		
		full_path = os.path.join(local_folder, file)
		relative_path = os.path.relpath(full_path)
		db_path = '/'+relative_path
		
		if not file in processed_files and not os.path.isdir(file) and not file.startswith('.') and file.endswith('.py'):
		
			if VERBOSE_LOGGING == True:
				print('Searching "%s" for "%s"' % (dropbox_dir, file))
			found = client.search(dropbox_dir, file)
			
			if found:
				print("File found on Dropbox, this shouldn't happen! Skipping %s..." % file)
			else:
				if VERBOSE_LOGGING == True:
					pp.pprint(file)
					
				if file in file_details:
					details = file_details[file]
				else:
					details = {}
				print(details)
				
				details = upload(relative_path, details, client, None )
				file_details[relative_path] = details
				write_sync_state(file_details)
				
		elif not db_path in dropbox_dirs and os.path.isdir(file) and not file.startswith('.') and not file == SYNC_STATE_FOLDER:
			local_dirs.append(db_path)
			
			
	#process the directories
	for folder in dropbox_dirs:
		if VERBOSE_LOGGING == True:
			print('Processing dropbox dir %s from %s' % (folder, dropbox_dir))
		process_folder(client, folder, file_details)
			
	for folder in local_dirs:
		if VERBOSE_LOGGING == True:
			print('Processing local dir %s from %s' % (folder, dropbox_dir))
		process_folder(client, folder, file_details)
			
def update_file_details(file_details, dropbox_metadata):
	file_details['revision'] = dropbox_metadata['revision']
	file_details['rev'] = dropbox_metadata['rev']
	file_details['modified'] = dropbox_metadata['modified']
	file_details['path'] = dropbox_metadata['path']
	return file_details
	
def write_sync_state(file_details):
	# Write sync state file
	sync_status_file = os.path.join(SYNC_STATE_FOLDER, 'file.cache.txt')
	
	if VERBOSE_LOGGING:
		print('Writing sync state to %s' % sync_status_file)
	
	with open(sync_status_file, 'w') as output_file:
		json.dump(file_details, output_file)

def main():

	# Process any supplied arguments
	global VERBOSE_LOGGING
	for argument in sys.argv:
		if argument == '-v':
			VERBOSE_LOGGING = True
	
	# Load the current sync status file, if it exists.
	sync_status_file = os.path.join(SYNC_STATE_FOLDER, 'file.cache.txt')
	
	if not os.path.exists(SYNC_STATE_FOLDER):
		os.mkdir(SYNC_STATE_FOLDER)
	if os.path.exists(sync_status_file):
		with open(sync_status_file, 'r') as input_file:
			file_details = json.load(input_file)
	else:
		file_details = {}
		
	if VERBOSE_LOGGING == True:
		print("File Details: ")
		pp.pprint(file_details)
		
	#configure dropbox
	sess = dropbox.session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
	configure_token(sess)
	client = dropbox.client.DropboxClient(sess)

	print("linked account: %s" % client.account_info()['display_name'])
	#pp.pprint (client.account_info())

	process_folder(client, '/', file_details)
				
	# Write sync state file
	write_sync_state(file_details)


if __name__ == "__main__":
	print('Begin Dropbox sync')
	main()
	print('Dropbox sync done!')
