from __future__ import print_function
# cosing: utf-8

# https://forum.omz-software.com/topic/1848/working-copy-integration-sidebar/23

# https://github.com/ahenry91/wc_sync

## Installation

# 1. Clone/download this repo to pythonista.
# 3. Go to Working Copy, Allow URL actions, and copy the URL key.
# 4. Run Working_Copy_Sync and paste in your URL key from Working Copy.
# 5. Add to quick actions menu to access from within other files

## Notes

# Each action (other than "Clone" Repo) uses your current file and working directory to determine which repo to update in Working Copy. Because of this, repos must live in the home (Documents) directory and cannot be nested under other folders. 

# Since Pythonista 2.0 cannot (as of right now) present a view as a sidebar anymore, the view has been changed to a modal. This also provided the opportunity to spell out what each button does.
import editor
import os
import console
import webbrowser as wb
import urllib
import base64
import keychain
import sys
import errno
import zipfile
import json
import dialogs
import shutil
from collections import OrderedDict

class WorkingCopySync():
	
	def __init__(self):
		self.key = self._get_key()
		self.install_path = self._find_install_path()
		self.repo, self.path = self._get_repo_info()
		
	def _get_key(self):
		''' Retrieve the working copy key or prompt for a new one. 
		'''
		key = keychain.get_password('wcSync', 'xcallback')
		if not key:
			key = console.password_alert('Working Copy Key')
			keychain.set_password('wcSync', 'xcallback', key)
		return key
	
	def _find_install_path(self):
		''' Dynamically find the installation path for the script
		'''
		app_dir = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))
		home_dir = os.path.join(os.environ['HOME'], 'Documents')
		return os.path.relpath(app_dir, home_dir)
	
	def _get_repo_info(self):
		documentsDir = os.path.expanduser('~/Documents')
		info = editor.get_path()
		fullPath = info[len(documentsDir)+1:] # get the relative path and remove the leading /
		print(fullPath)
		path = fullPath.split('/',1)[1]
		repo = fullPath.split('/',1)[0]
		return repo, path			
		
	def _send_to_working_copy(self, action, payload, x_callback_enabled=True):
		payload['key'] = self.key
		if x_callback_enabled:
			url = 'working-copy://x-callback-url/{action}/?{payload}'
		else:
			url = 'working-copy://{action}/?{payload}'
		urlencoded_payload = urllib.urlencode(payload).replace('+', '%20')
		url = url.format(action=action, payload=urlencoded_payload)
		wb.open(url)
		
	def _get_repo_list(self):
		action = 'repos'
		payload = {
			'x-success': 'pythonista://{install_path}/Working_Copy_Sync.py?action=run&argv=repo_list&argv='.format(install_path=self.install_path)
		}
		self._send_to_working_copy(action, payload)

	def copy_repo_from_wc(self, repo_list=None):
		''' copy a repo to the local filesystem 
		'''
		if not repo_list:
			self._get_repo_list()
		else:
			repo_name = dialogs.list_dialog(title='Select repo', items=repo_list)
			if repo_name:
				action = 'zip'
				payload = {
					'repo': repo_name,
					'x-success': 'pythonista://{install_path}/Working_Copy_Sync.py?action=run&argv=copy_repo&argv={repo_name}&argv='.format(install_path=self.install_path, repo_name=repo_name)
				}
				self._send_to_working_copy(action, payload)
			
	def _push_file_to_wc(self, path, contents):
		action = 'write'
		payload = {
			'repo': self.repo,
			'path': path,
			'text': contents,
			'x-success': 'pythonista://{repo}/{path}?'.format(repo=self.repo, path=path)
		}
		self._send_to_working_copy(action, payload)
			
	def push_current_file_to_wc(self):
		self._push_file_to_wc(self.path, editor.get_text())
		
	def push_pyui_to_wc(self):
		pyui_path, pyui_contents = self._get_pyui_contents_for_file()
		if not pyui_contents:
			console.alert('No PYUI file associated. Now say you\'re sorry.', button1='I\'m sorry.', hide_cancel_button=True)
		else:
			self._push_file_to_wc(pyui_path, pyui_contents)
		
	def _get_pyui_contents_for_file(self):
		rel_pyui_path = self.path + 'ui'
		full_pyui_path = os.path.join(os.path.expanduser('~/Documents'), os.path.join(self.repo, rel_pyui_path))
		try:
			with open(full_pyui_path) as f:
				return rel_pyui_path, f.read()
		except IOError:
			return None, None
			
	def overwrite_with_wc_copy(self):
		action = 'read'
		payload = {
			'repo': self.repo,
			'path': self.path,
			'base64': '1',
			'x-success': 'pythonista://{install_path}/Working_Copy_Sync.py?action=run&argv=overwrite_file&argv={full_path}&argv='.format(install_path=self.install_path, full_path=os.path.join(self.repo, self.path))
		}
		self._send_to_working_copy(action, payload)
		
	def open_repo_in_wc(self):
		action = 'open'
		payload = {
			'repo': self.repo
		}
		self._send_to_working_copy(action, payload)

	def present(self):
		action_mapping = OrderedDict()
		action_mapping['CLONE		- Copy repo from Working Copy'] = self.copy_repo_from_wc
		action_mapping['FETCH		- Overwrite file with WC version'] = self.overwrite_with_wc_copy
		action_mapping['PUSH		- Send file to WC'] = self.push_current_file_to_wc
		action_mapping['PUSH UI	- Send associated PYUI to WC'] = self.push_pyui_to_wc
		action_mapping['OPEN		- Open repo in WC'] = self.open_repo_in_wc

		actions = []	
		for action in OrderedDict(action_mapping):
			actions.append(action)
		action = dialogs.list_dialog(title='Choose action', items=actions)
		if action:
			action_mapping[action]()
		
	def urlscheme_copy_repo_from_wc(self, path, b64_contents):
		tmp_zip_location = self.install_path + 'repo.zip'
		
		try:
			os.makedirs(os.path.join(os.path.expanduser('~/Documents'), path))
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise e
			console.alert('Overwriting existing directory', button1='Continue')
			shutil.rmtree(os.path.join(os.path.expanduser('~/Documents'), path))

		zip_file_location = os.path.join(os.path.expanduser('~/Documents'), tmp_zip_location)
		with open(zip_file_location, 'w') as f:
			f.write(base64.b64decode(b64_contents))
			
		zip_file = zipfile.ZipFile(zip_file_location)	
		zip_file.extractall(os.path.join(os.path.expanduser('~/Documents'), path))
		os.remove(zip_file_location)
		console.hud_alert(path + ' Downloaded')
		
	def urlscheme_overwrite_file_with_wc_copy(self, path, b64_contents):
		text = base64.b64decode(b64_contents)
		
		try:
			os.makedirs(os.path.join(os.path.expanduser('~/Documents'), path))
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise e
				
		full_file_path = os.path.join(os.path.expanduser('~/Documents'), path)
		with open(full_file_path, 'w') as f:
			f.write(text)
			
		editor.open_file(path)
		console.hud_alert(path +' Updated')
		
			
def main():
	wc = WorkingCopySync()
	if len(sys.argv) <= 1:
		wc.present()
	else:
		action = sys.argv[1]
		if action == 'copy_repo':
			wc.urlscheme_copy_repo_from_wc(sys.argv[2], sys.argv[3])
		elif action == 'overwrite_file':
			wc.urlscheme_overwrite_file_with_wc_copy(sys.argv[2], sys.argv[3])
		elif action == 'repo_list':
			repo_list = []
			for repo in json.loads(sys.argv[2]):
				repo_list.append(repo['name'])
			wc.copy_repo_from_wc(repo_list=repo_list)
		else:
			console.alert('Not a valid URL scheme action. Now say you\'re sorry.', button1='I\'m sorry.', hide_cancel_button=True)
		
if __name__ == "__main__":
	main()