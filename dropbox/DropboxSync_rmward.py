https://github.com/rmward/pythonista-dropbox-sync

import os, sys, pickle, console, re
 
sys.path += ['lib']
import dropboxsetup

# dropbox_sync
# by Michelle L. Gill, michelle@michellelynngill.com
# requires my dropboxsetup module (https://gist.github.com/8311046)

# Change log
# 2013/01/07: initial version
# 2013/01/09: added regex filtering

##################################################################
#                                                                #
#                  User specified parameters                     #
#                                                                #
##################################################################

####### REGEX FILTERS NOT FULLY TESTED YET. USE DEBUG FIRST #######
# only files which match regexes in this list will be considered
# leave empty to consider all files
include_list = []

# then files which match regular expressions in this list will be removed 
# leave empty for no exclusions
# empty directories are not uploaded
exclude_list = []

# set this to true to test regular expressions instead of uploading
debug_regex = False

##################################################################
#                                                                #
#      Probably don't need to change anything below this point   #
#                                                                #
##################################################################


STATE_FILE = '.dropbox_state'
 
class dropbox_state:
	def __init__(self):
		self.cursor = None
		self.local_files = {}
		self.remote_files = {}
		self.app_key=""
		self.app_secret=""
		self.token_file_name=""

	def get_app_key(self):
		return self.app_key		

	def set_app_key(self, name):
		self.app_key=name

	def get_app_secret(self):
		return self.app_secret

	def set_app_secret(self, name): 
		self.app_secret=name

	def get_token_file_name(self): 
		return self.token_file_name
 
	def set_token_file_name(self, name): 
		self.token_file_name=name

	# use ignore_path to prevent download of recently uploaded files 
	def execute_delta(self, client, ignore_path = None):
		delta = client.delta(self.cursor)
		self.cursor = delta['cursor']
		
		for entry in delta['entries']:
			path = entry[0][1:]
			meta = entry[1]
			
			# this skips the path if we just uploaded it
			if path != ignore_path:
				if meta != None:
					path = meta['path'][1:] # caps sensitive
					if meta['is_dir']:
						print '\n\tMaking Directory:',path
						self.makedir_local(path)
					elif path not in self.remote_files:
						print '\n\tNot in local'
						self.download(client, path)
					elif meta['rev'] != self.remote_files[path]['rev']:
						print '\n\tOutdated revision'
						self.download(client, path)
				# remove file or directory
				else: 
					if os.path.isdir(path):
						print '\n\tRemoving Directory:', path
						os.removedirs(path)
					elif os.path.isfile(path):
						print '\n\tRemoving File:', path
						os.remove(path)
						
						del self.local_files[path]
						del self.remote_files[path]
					else:
						pass # file already doesn't exist localy
 
	# makes dirs if necessary, downloads, and adds to local state data
	def download(self, client, path):
		print '\tDownloading:', path
		# TODO: what if there is a folder there...?
		head, tail = os.path.split(path)
		# make the folder if it doesn't exist yet
		if not os.path.exists(head) and head != '':
			os.makedirs(head)
		#open file to write
		local = open(path,'w')
		remote, meta = client.get_file_and_metadata(os.path.join('/',path))
		local.write(remote.read())
		#clean up
		remote.close()
		local.close()
		# add to local repository
		self.local_files[path] = {'modified': os.path.getmtime(path)}
		self.remote_files[path] = meta
	
	def upload(self, client, path):
		print '\tUploading:', path
		local = open(path,'r')
		meta = client.put_file(os.path.join('/',path), local, True)
		local.close()
		
		self.local_files[path] = {'modified': os.path.getmtime(path)}
		self.remote_files[path] = meta
		
		# clean out the delta for the file upload
		self.execute_delta(client, ignore_path=meta['path'])
	
	def delete(self, client, path):
		print '\tFile deleted locally. Deleting on Dropbox:',path
		try:
			client.file_delete(path)
		except:
			# file was probably already deleted
			print '\tFile already removed from Dropbox'
			
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
	def _listfiles(self, client, path = '/'):
		meta = client.metadata(path)
		filelist = []
		
		for item in meta['contents']:
			if item['is_dir']:
				filelist += self._listfiles(client,item['path'])
			else:
				filelist.append(item['path'])
		return filelist
				
	def download_all(self, client, path = '/'):
		filelist = self._listfiles(client)
		for file in filelist:
			self.download(client, file[1:])	# trim root slash
	
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
	fyle = open(STATE_FILE,'r')
	state = pickle.load(fyle)
	fyle.close()
	
	return state
 
def savestate(state):
	fyle = open(STATE_FILE,'w')
	pickle.dump(state,fyle)
	fyle.close()
	
if __name__ == '__main__':
	console.show_activity()
	
	print """
****************************************
*     Dropbox File Syncronization      *
****************************************"""
	
	print '\nLoading local state'
	# lets see if we can unpickle
	try:
		state = loadstate()
		_, client = dropboxsetup.init(state.get_token_filename(), state.get_app_key(), state.get_app_secret())
	except:
		print '\nCannot find state file. ***Making new local state***\n'
		# Aaaah, we have nothing, probably first run
		state = dropbox_state()

		print("We need a few setup details.\n")
		print("What do you want to call the Dropbox token file?")
		temp_input=raw_input()
		state.set_token_file_name(temp_input)
		print("What's your Dropbox app key?")
		temp_input=raw_input()
		state.set_app_key(temp_input)		
		print("What's your Dropbox app secret?")
		temp_input=raw_input()
		state.set_app_secret(temp_input)
		print("Cool. We're ready to proceed.\n\n")
	
		_, client = dropboxsetup.init(state.get_token_file_name(), state.get_app_key(), state.get_app_secret())
		
		print '\nDownloading everything from Dropbox'
		# no way to check what we have locally is newer, gratuitous dl
		state.download_all(client)
 
	print '\nUpdating state from Dropbox'
	state.execute_delta(client)
		
	
	print '\nChecking for new or updated local files'
	# back to business, lets see if there is anything new or changed localy
	dir_match=re.search(r'(/private/var/mobile/Applications/[0-9A-Z\\-]+/Documents)/.*', os.getcwd())
	pythonista_root=dir_match.group(1)

	filelist = []
	
	for root, dirnames, filenames in os.walk(pythonista_root):
		for filename in filenames:
			if filename != STATE_FILE:
				filelist.append( os.path.join(root, filename))
	
	####### REGEX FILTERS NOT FULLY TESTED YET #######
	filelist = set(filelist)
	if debug_regex:
		allfiles = filelist

	# remove all files not in the includes list
	if len(include_list) >= 1:
		filelistinc = set()
		for reg in include_list:
			regc = re.compile(reg)
			filelistinc = filelistinc | set([x for x in filelist if re.search(regc,x)])

		filelist = filelistinc
	
	if debug_regex:
		incfiles_keep = filelist
		incfiles_filt = allfiles - incfiles_keep

	# remove the excludes
	for reg in exclude_list:
		regc = re.compile(reg)
		filelist = filelist - set([x for x in filelist if re.search(regc,x)])

	if debug_regex:
		excfiles_keep = filelist
		excfiles_filt = incfiles_keep - excfiles_keep

		print '\nThe following files were removed from sync list because they did not match include filters:\n'
		print incfiles_filt
		print '\nThe following files were then removed from sync list because they matched exclude filters:\n'
		print excfiles_filt
		print '\n The following files remain in the sync list after filtering:\n'
		print filelist
		
	else:
		filelist = list(filelist)

		for file in filelist:
			state.check_state(client,file)
		
		print '\nChecking for deleted local files'
		old_list = state.local_files.keys()
		for file in old_list:
			if file not in filelist:
				state.delete(client, file)
		
		print '\nSaving local state'
		savestate(state)
		
		print '\nSync complete'
	
