# See: http://www.devwithimagination.com/2014/05/11/pythonista-dropbox-sync

import webbrowser, os
import dropbox
import hashlib
import json
import difflib
import sys
import logging
import re
import console

# Program, do not edit from here

# custom logging level
FINE = 15

# file locations used by the program
PYTHONISTA_DOC_DIR = os.path.expanduser('~/Documents')
SYNC_FOLDER_NAME = 'dropbox_sync'
SYNC_STATE_FOLDER = os.path.join(PYTHONISTA_DOC_DIR, SYNC_FOLDER_NAME)
SYNC_STATE_FILENAME = 'file.cache.txt'
CONFIG_FILENAME = 'PythonistaDropbox.conf'
CONFIG_FILEPATH = os.path.join(SYNC_STATE_FOLDER, CONFIG_FILENAME)

# default file extensions which will be processed
DEFAULT_FILE_EXTENSIONS = ['.py', '.pyui', '.txt', '.conf']

# default list of files that shouldn't be synced
DEFAULT_SKIP_FILES = [os.path.join(SYNC_FOLDER_NAME, SYNC_STATE_FILENAME)]

# dict holding options the user has chosen to remember
REMEMBER_OPTIONS = {}

# Method to get the MD5 Hash of the file with the supplied file name.
def getHash(file_name):
	# Open,close, read file and calculate MD5 on its contents
	with open(os.path.join(PYTHONISTA_DOC_DIR, file_name)) as file_to_check:
		# pipe contents of the file through
		return hashlib.md5(file_to_check.read()).hexdigest()

# Helper method to determine if a local file is eligible for sync
def can_sync_local_file(config, file):

	relative_path = os.path.relpath(file, PYTHONISTA_DOC_DIR)
	file_name = os.path.basename(file)

	if not relative_path in config['skip_files'] and not file_name.startswith('.') and not os.path.isdir(file):
		
		file_ext = os.path.splitext(file)[1]
			
		if file_ext in (config['file_extensions']) or [m.group(0) for l in config['file_extensions'] for m in [re.match('[\.]?\*',l)] if m]:
			return True
	
	return False

# Method to determine if the supplied local folder contains any files which would be eligible for sync
def can_sync_local_directory(config, local_folder):
	
	dir_name = os.path.basename(local_folder)
	
	if os.path.exists(local_folder) and not os.path.relpath(local_folder, PYTHONISTA_DOC_DIR) in config['skip_files'] and not dir_name.startswith('.'):
		files = os.listdir(local_folder)
		for current_file in files:
		
			full_path = os.path.join(local_folder, current_file)
			relative_path = os.path.relpath(full_path, PYTHONISTA_DOC_DIR)
			db_path = '/'+relative_path

			if can_sync_local_file(config, full_path):
				return True
			
			elif os.path.isdir(full_path):
			
					files_found = can_sync_local_directory(config, full_path)
					
					if files_found:
						# Something in the directory needs to be synced
						return True


	logging.debug('Directory %s does not contain any files for sync', local_folder)
	return False
		
# Write the updated configuration
def write_configuration(config):
	with open(CONFIG_FILEPATH, 'w') as config_file:
			json.dump(config, config_file, indent=1)

# Method to configure the supplied dropbox session.
# This will use cached OAUTH credentials if they have been stored, otherwise the
# user will be put through the Dropbox authentication process.
def configure_token(dropbox_session, configuration):
	
	if 'token_key' in configuration and 'token_secret' in configuration:
		# values exist in our config already
		dropbox_session.set_token(configuration['token_key'], configuration['token_secret'])
	else:
		setup_new_auth_token(dropbox_session, configuration)

# Method to set up a new Dropbox OAUTH token.
# This will take the user through the required steps to authenticate.
def setup_new_auth_token(sess, configuration):
	request_token = sess.obtain_request_token()
	url = sess.build_authorize_url(request_token)

	# Make the user sign in and authorize this token
	logging.debug('url: %s', url)
	logging.info('Please visit this website and press the "Allow" button, then hit "Enter" here.')
	webbrowser.open(url)
	raw_input()
	# This will fail if the user didn't visit the above URL and hit 'Allow'
	access_token = sess.obtain_access_token(request_token)
	# update configuration with token
	configuration['token_key'] = access_token.key
	configuration['token_secret'] = access_token.secret
	
	write_configuration(configuration)

def upload(file, details, client, parent_revision):
	logging.log(FINE, 'Trying to upload %s', file)
	details['md5hash'] = getHash(file)
	logging.log(FINE, 'New MD5 hash: %s', details['md5hash'])

	with open(os.path.join(PYTHONISTA_DOC_DIR, file), 'r') as in_file:
		response = client.put_file(file, in_file, False, parent_revision)
	
	logging.debug('Response: %s', response)
	details = update_file_details(details, response)

	logging.info('Uploaded %s', file)

	return details

def download(dest_path, dropbox_metadata, details, client):
	with open(os.path.join(PYTHONISTA_DOC_DIR, dest_path), 'w') as out_file:
		out_file.write(client.get_file(dropbox_metadata['path']).read())

	details['md5hash'] = getHash(dest_path)
	logging.log(FINE, 'New MD5 hash: %s', details['md5hash'])
	logging.info('Downloaded %s', dest_path)
	return update_file_details(details, dropbox_metadata)

def process_folder(config, client, dropbox_dir, file_details):

	# Get the metadata for the directory being processed (dropbox_dir).
	# If the directory does not exist on Dropbox it will be created.
	try:
		folder_metadata = client.metadata(dropbox_dir)

		logging.debug('metadata: %s', folder_metadata)
		
		if 'is_deleted' in folder_metadata:
			# directory is deleted, create
			client.file_create_folder(dropbox_dir)
			folder_metadata = client.metadata(dropbox_dir)			
		
	except dropbox.rest.ErrorResponse as error:
		logging.debug(error.status)
		if error.status == 404:
			client.file_create_folder(dropbox_dir)
			folder_metadata = client.metadata(dropbox_dir)
		else:
			logging.exception(error)
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
		
		file_ext = os.path.splitext(file_name)[1]
		
		if file['is_dir'] == False and (file_ext in config['file_extensions'] or [m.group(0) for l in config['file_extensions'] for m in [re.match('[\.]?\*',l)] if m]):

			if not os.path.exists(os.path.join(PYTHONISTA_DOC_DIR, dropbox_path)):
				logging.info('Processing Dropbox file %s (%s)', file['path'], dropbox_path)
				
				try:


					if dropbox_path in file_details:
						# in cache but file no longer locally exists
						details = file_details[dropbox_path]

						if 'SYNC_NO_LOCAL' in REMEMBER_OPTIONS:
							prev_choice = REMEMBER_OPTIONS['SYNC_NO_LOCAL']
						else:
							prev_choice = ''
						
						if prev_choice in ('la', 'da', 'sa'):
							choice = prev_choice[0]
						else:

							choice = raw_input('''File %s is in the sync cache and on Dropbox, but no longer exists locally. (Default Delete):
Delete From Dropbox (d) [All in this state (da)]
Download File (l) [All in this state (da)]
Skip (s) [All in this state (sa)]
''' % file['path']).lower()
						
						# remember options if necessary
						if choice in ('la', 'da', 'sa'):
							REMEMBER_OPTIONS['SYNC_NO_LOCAL'] = choice
							choice = choice[0]
							
						if (choice == 'l'):
							download_file = True
						elif (choice == 'd' or not choice):
							# Default is 'del'
							download_file = False

							#delete the dropbox copy
							client.file_delete(file['path'])
							file_details.remove(dropbox_path)

					else:
						details = {}
						download_file = True

					if download_file:
						logging.info('Downloading file %s (%s)', file['path'], dropbox_path)
						logging.debug(details)

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

					logging.debug('Held details are: %s', details)

					if details['revision'] == file['revision']:
						# same revision
						current_hash = getHash(dropbox_path)

						logging.debug('New hash: %s, Old hash: %s', current_hash, details['md5hash'])

						if current_hash == details['md5hash']:
							logging.log(FINE, 'File "%s" not changed.', dropbox_path)
						else:
							logging.log(FINE, 'File "%s" updated locally, uploading...', dropbox_path)

							details = upload(dropbox_path, details, client, file['rev'])
							file_details[dropbox_path] = details

						processed_files.append(file_name)
					else:
						#different revision
						logging.log(FINE, 'Revision of "%s" changed from %s to %s. ', dropbox_path, details['revision'], file['revision'])

						current_hash = getHash(dropbox_path)

						logging.debug('File %s. New hash: %s, Old hash: %s', dropbox_path, current_hash, details['md5hash'])

						if current_hash == details['md5hash']:
							logging.log(FINE, 'File "%s" updated remotely. Downloading...', dropbox_path)

							details = download(dropbox_path, file, details, client)
							file_details[dropbox_path] = details
						else:
							
							if 'UPDATED_BOTH' in REMEMBER_OPTIONS:
								prev_choice = REMEMBER_OPTIONS['UPDATED_BOTH']
							else:
								prev_choice = ''
						
							if prev_choice in ('la', 'da', 'sa'):
								choice = prev_choice[0]
							else:
								choice = raw_input('''File %s has been updated both locally and on Dropbox. (Default Skip) Overwrite: 
Dropbox Copy (d) [All in this state (da)]
Local Copy (l) [All in this state (la)]
Skip (s) [All in this state (sa)]
''' % file['path']).lower()
							
							# remember options if necessary
							if choice in ('la', 'da', 'sa'):
								REMEMBER_OPTIONS['UPDATED_BOTH'] = choice
								choice = choice[0]

							if choice == 'd':
								logging.log(FINE, 'Overwriting Dropbox Copy of %s', file)
								details = upload(dropbox_path, details, client, file['rev'])
								file_details[dropbox_path] = details
							elif choice == 'l':
								logging.log(FINE, 'Overwriting Local Copy of %s', file)
								details = download(dropbox_path, file, details, client)
								file_details[dropbox_path] = details


				else:
					# Not in cache, but exists on dropbox and local, need to prompt user
					if 'NO_SYNC_BOTH' in REMEMBER_OPTIONS:
						prev_choice = REMEMBER_OPTIONS['NO_SYNC_BOTH']
					else:
						prev_choice = ''
						
					if prev_choice in ('la', 'da', 'sa'):
						choice = prev_choice[0]
					else:
						choice = raw_input('''File %s is not in the sync cache but exists both locally and on dropbox. (Default Skip) Overwrite:
Dropbox Copy (d) [All in this state (da)]
Local Copy (l) [All in this state (la)]
Skip (s) [All in this state (sa)]
 ''' % file['path']).lower()

					# remember options if necessary
					if choice in ('la', 'da', 'sa'):
						REMEMBER_OPTIONS['NO_SYNC_BOTH'] = choice
						choice = choice[0]

					details = {}
					if choice == 'd':
						logging.log(FINE, 'Overwriting Dropbox Copy of %s', file)
						details = upload(dropbox_path, details, client, file['rev'])
						file_details[dropbox_path] = details
					elif choice == 'l':
						logging.log(FINE, 'Overwriting Local Copy of %s', file)
						details = download(dropbox_path, file, details, client)
						file_details[dropbox_path] = details
					else:
						logging.log(FINE, 'Skipping processing for file %s', file)

				# Finished dealing with this file, update the sync state and mark this file as processed.
				write_sync_state(file_details)
				processed_files.append(file_name)
		elif file['is_dir'] and 'is_deleted' not in file:
			dropbox_dirs.append(file['path'])


	# go through the files that are local but not on Dropbox, upload these.
	files = os.listdir(local_folder)
	for file in files:

		full_path = os.path.join(local_folder, file)
		relative_path = os.path.relpath(full_path, PYTHONISTA_DOC_DIR)
		db_path = '/'+relative_path

		if not file in processed_files and not relative_path in config['skip_files'] and not os.path.isdir(full_path) and not file.startswith('.'):
			
			filename, file_ext = os.path.splitext(file)
			
			if file_ext in (config['file_extensions']) or [m.group(0) for l in config['file_extensions'] for m in [re.match('[\.]?\*',l)] if m]:
					
					
				logging.debug('Searching "%s" for "%s"', dropbox_dir, file)
				# this search includes dropbox_dir AND CHILD DIRS!
				search_results = client.search(dropbox_dir, file)
				
				logging.debug(search_results)
				
				found = False
				for single_result in search_results:
					if single_result['path'] == db_path:
						found = True

				if found:
					logging.warning("File found on Dropbox, this shouldn't happen! Skipping %s...", file)
				else:
					logging.debug(relative_path)

					upload_file = False
					
					# check if an upload or a local delete is required
					if relative_path in file_details:
						# File is not in dropbox but is in sync cache
						details = file_details[relative_path]
						
						if 'SYNC_NO_DROP' in REMEMBER_OPTIONS:
							prev_choice = REMEMBER_OPTIONS['SYNC_NO_DROP']
						else:
							prev_choice = ''
							
						if prev_choice in ('da', 'ua', 'sa'):
							choice = prev_choice[0]
						else:
							choice = raw_input('''File %s is in the sync cache but no longer on Dropbox. (Default Delete):
Delete local file (d) [All in this state (da)]
Upload File (u) [All in this state (ua)
Skip (s) [All in this state (sa)]
''' % relative_path).lower()
							
						# remember options if necessary
						if choice in ('ua', 'da', 'sa'):
							REMEMBER_OPTIONS['SYNC_NO_DROP'] = choice
							choice = choice[0]
						
						if choice == 'u':
							upload_file = True
						elif (choice == 'd' or not choice):
							# delete file
							os.remove(full_path)
							
							# update sync state
							del file_details[relative_path]
							write_sync_state(file_details)
					else:
						details = {}
						upload_file = True
						
					logging.debug('Details were %s', details)
					
					# upload the file
					if upload_file:
						details = upload(relative_path, details, client, None )
						file_details[relative_path] = details
						write_sync_state(file_details)
				
			else:
				logging.debug("Skipping extension %s", file_ext)

		elif not db_path in dropbox_dirs and os.path.isdir(full_path) and can_sync_local_directory(config, full_path):
			local_dirs.append(db_path)


	#process the directories
	for folder in dropbox_dirs:
		logging.debug('Processing dropbox dir %s from %s', folder, dropbox_dir)
		if folder[1:] not in config['skip_files']:
			process_folder(config, client, folder, file_details)
		else:
			logging.log(FINE, 'Skipping dropbox directory %s', folder)

	for folder in local_dirs:
		logging.debug('Processing local dir %s from %s', folder, dropbox_dir)
		if folder[1:] not in config['skip_files']:
			process_folder(config, client, folder, file_details)
		else:
			logging.log(FINE, 'Skipping local directory %s', folder)
			
	# delete the folder if empty
	folder_metadata = client.metadata(dropbox_dir)
	if len(folder_metadata['contents']) == 0 and 'is_deleted' not in folder_metadata:
		# empty remote directory - delete
		logging.info('Remote directory %s is empty, deleting...', dropbox_dir)
		logging.debug('Pre-delete metadata %s', folder_metadata)
		client.file_delete(dropbox_dir)



def update_file_details(file_details, dropbox_metadata):
	for key in 'revision rev modified path'.split():
		file_details[key] = dropbox_metadata[key]
	return file_details

def write_sync_state(file_details):
	# Write sync state file
	sync_status_file = os.path.join(SYNC_STATE_FOLDER, SYNC_STATE_FILENAME)

	logging.debug('Writing sync state to %s', sync_status_file)

	with open(sync_status_file, 'w') as output_file:
		json.dump(file_details, output_file)

# prompt user for additional (optional) configuration options
def setup_user_configuration(prompt, configuration):
	
	if prompt:
		
		configuration['file_extensions'] = raw_input('''What file extensions should be synced? New extensions must be prefixed with a dot, and be comma separated. (These will be included by default %s)
''' % DEFAULT_FILE_EXTENSIONS).replace(', ',',').split(',')
		
		logging.debug(input)
		
		configuration['skip_files'] = raw_input('''What files should not be synced? Paths should be relative to the root and be comma separated.
''').replace(', ',',').split(',')
	
		write_configuration(configuration)
	
	# add missing options if not user configured
	if 'file_extensions' not in configuration:
		configuration['file_extensions'] = []
		
	for ext in DEFAULT_FILE_EXTENSIONS:
		if ext not in configuration['file_extensions']:
			configuration['file_extensions'].append(ext)
		
	logging.log(FINE, 'File extensions: %s', configuration['file_extensions'])
		
	if 'skip_files' not in configuration:
		configuration['skip_files'] = []
		
	for file in DEFAULT_SKIP_FILES:
		if file not in configuration['skip_files']:
			configuration['skip_files'].append(file)
			
	logging.log(FINE, 'Skip files: %s', configuration['skip_files'])

# Load the configuration file, if it exists. 
# if a configuration file does not exist this will prompt
# the user for inital configuration values		
def setup_configuration():
	
	if not os.path.exists(SYNC_STATE_FOLDER):
		os.mkdir(SYNC_STATE_FOLDER)
	if os.path.exists(CONFIG_FILEPATH):
		with open(CONFIG_FILEPATH, 'r') as config_file:
			config = json.load(config_file)
	else:
		logging.log(FINE, 'Configuration file missing')
		config = {}
		
		logging.info('Get your app key and secret from the Dropbox developer website')
		
		config['APP_KEY'] = raw_input('''Enter your app key
''')
		config['APP_SECRET'] = raw_input('''Enter your app secret
''')
		
		# ACCESS_TYPE can be 'dropbox' or 'app_folder' as configured for your app
		config['ACCESS_TYPE'] = 'app_folder'
		
		
		# Write the config file back
		write_configuration(config)
			
	return config
	


# Load the current sync status file, if it exists, and return the contents.
# if the file does not exist an empty object will be returned. 
def load_sync_state():
	
	sync_status_file = os.path.join(SYNC_STATE_FOLDER, SYNC_STATE_FILENAME)

	if not os.path.exists(SYNC_STATE_FOLDER):
		os.mkdir(SYNC_STATE_FOLDER)
	if os.path.exists(sync_status_file):
		with open(sync_status_file, 'r') as input_file:
			file_details = json.load(input_file)
	else:
		file_details = {}

	logging.debug('File Details: %s', file_details)
	
	return file_details
	

def main():

	# Process any supplied arguments
	log_level = 'INFO'
	update_config = False
	
	for argument in sys.argv:
		if argument.lower() == '-v':
			log_level = 'FINE'
		elif argument.lower() == '-vv':
			log_level = 'DEBUG'
		elif argument.lower() == '-c':
			update_config = True
			
	# configure logging
	log_format = "%(message)s"
	
	logging.addLevelName(FINE, 'FINE')
	for handler in logging.getLogger().handlers:
		logging.getLogger().removeHandler(handler)
	logging.basicConfig(format=log_format, level=log_level)
	
	
	# disable dimming the screen
	console.set_idle_timer_disabled(True)

	# Load the current sync status file
	file_details = load_sync_state()
		
	# Load the initial configuration
	config = setup_configuration()
	
	# set up user configuration options
	setup_user_configuration(update_config, config)
		
	logging.info('Begin Dropbox sync')

	#configure dropbox
	sess = dropbox.session.DropboxSession(config['APP_KEY'], config['APP_SECRET'], config['ACCESS_TYPE'])
	configure_token(sess, config)
	client = dropbox.client.DropboxClient(sess)

	logging.info('linked account: %s', client.account_info()['display_name'])

	process_folder(config, client, '/', file_details)

	# Write sync state file
	write_sync_state(file_details)
	
	# re-enable dimming the screen
	console.set_idle_timer_disabled(False)


if __name__ == "__main__":
	main()
	logging.info('Dropbox sync done!')
	