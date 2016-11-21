# coding: utf-8

# https://github.com/ahenry91/wc_sync/blob/master/Working_Copy_Sync.py

# Installation

# 1. Clone/download this repo to pythonista.
# 2. Go to Working Copy, Allow URL actions, and copy the URL key.
# 3. Run Working_Copy_Sync and paste in your URL key from Working Copy.
# 4. Add to quick actions menu to access from within other files

# Pythonista/Working Copy X-Callback URLs do not like spaces in the file/directory names (when cloning, fetching, pushing). Try to avoid any spaces when naming files and directories.

import base64
import console
import dialogs
import editor
import errno
import json
import keychain
import os
import shutil
import sys
import webbrowser as wb
import zipfile
from collections import OrderedDict

try:
	from urllib import urlencode
except:
	from urllib.parse import urlencode

DOCS_DIR = os.path.expanduser('~/Documents')
WC_FILENAME = os.path.split(__file__)[-1]
CONFIG_FILE = '.wcsync'

class WorkingCopySync():

	def __init__(self):
		self.key = self._get_key()
		self.install_path = self._find_install_path()
		self.config = self._get_config()
		self.repo, self.path = None, None
		if self.config: 
			self.repo = self.config['repo-name']
			# build the path relative to the repo-root
			self.path = editor.get_path()[len(self.config['repo-root'])+1:]
	
	@property
	def repo_path(self):
		return os.path.join(self.repo, self.path)		
		
	def _get_config(self, path=None):
		''' Dind the config file for the repo recursively.
				Don't look beyond the docs directory.
		'''
		config = None
		if not path: 
			path = os.path.dirname(editor.get_path())	
		config_path = os.path.join(path, CONFIG_FILE)
		if os.path.exists(config_path):
			with open(config_path) as f:
				config = json.loads(f.read())
				config['repo-root'] = path
		elif path != DOCS_DIR:
			new_path = os.path.abspath(os.path.join(path, '..'))
			config = self._get_config(new_path)
		return config

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
		return os.path.relpath(app_dir, DOCS_DIR)

	def _send_to_working_copy(self, action, payload, x_callback_enabled=True):
		x_callback = 'x-callback-url/' if x_callback_enabled else ''
		payload['key'] = self.key
		payload = urlencode(payload).replace('+', '%20')
		fmt = 'working-copy://{x_callback}{action}/?{payload}'
		url = fmt.format(x_callback=x_callback, action=action, payload=payload)
		wb.open(url)

	def _get_repo_list(self):
		action = 'repos'
		fmt = 'pythonista3://{install_path}/{wc_file}?action=run&argv=repo_list&argv='
		payload = {
			'x-success': fmt.format(install_path=self.install_path, wc_file=WC_FILENAME)
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
				fmt = 'pythonista3://{install_path}/{wc_file}?action=run&argv=copy_repo&argv={repo_name}&argv='
				payload = {
					'repo': repo_name,
					'x-success': fmt.format(install_path=self.install_path, repo_name=repo_name, wc_file=WC_FILENAME)
				}
				self._send_to_working_copy(action, payload)

	def _push_file_to_wc(self, path, contents):
		action = 'write'
		payload = {
			'repo': self.repo,
			'path': path,
			'text': contents,
			'x-success': 'pythonista3://{repo}/{path}?'.format(repo=self.repo, path=path)
		}
		self._send_to_working_copy(action, payload)

	def push_current_file_to_wc(self):
		self._push_file_to_wc(self.path, editor.get_text())

	def push_pyui_to_wc(self):
		pyui_path, pyui_contents = self._get_pyui_contents_for_file()
		if not pyui_contents:
			console.alert("No PYUI file associated. Now say you're sorry.",
				button1="I'm sorry.", hide_cancel_button=True)
		else:
			self._push_file_to_wc(pyui_path, pyui_contents)

	def _get_pyui_contents_for_file(self):
		rel_pyui_path = self.path + 'ui'
		full_pyui_path = os.path.join(DOCS_DIR, self.repo, rel_pyui_path)
		try:
			with open(full_pyui_path) as f:
				return rel_pyui_path, f.read()
		except IOError:
			return None, None

	def overwrite_with_wc_copy(self):
		action = 'read'
		fmt = 'pythonista3://{install_path}/{wc_file}?action=run&argv=overwrite_file&argv={path}&argv='
		payload = {
			'repo': self.repo,
			'path': self.path,
			'base64': '1',
			'x-success': fmt.format(install_path=self.install_path, path=editor.get_path(), wc_file=WC_FILENAME)
		}
		self._send_to_working_copy(action, payload)

	def open_repo_in_wc(self):
		action = 'open'
		payload = {
			'repo': self.repo
		}
		self._send_to_working_copy(action, payload)

	def present(self):
		actions = OrderedDict()
		actions['CLONE 	- Copy repo from Working Copy'] = self.copy_repo_from_wc
		if self.repo: 
			actions['FETCH 	- Overwrite file with WC version'] = self.overwrite_with_wc_copy
			actions['PUSH 		- Send file to WC'] = self.push_current_file_to_wc
			actions['PUSH UI 	- Send associated PYUI to WC'] = self.push_pyui_to_wc
			actions['OPEN 		- Open repo in WC'] = self.open_repo_in_wc
		action = dialogs.list_dialog(title='Choose action', items=[key for key in actions])
		if action:
			actions[action]()

	def urlscheme_copy_repo_from_wc(self, path, b64_contents):
		tmp_zip_location = self.install_path + 'repo.zip'
		dest = os.path.join(DOCS_DIR, path)
		try:
			os.makedirs(dest)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise e
			console.alert('Overwriting existing directory', button1='Continue')
			shutil.rmtree(dest)
		zip_file_location = os.path.join(DOCS_DIR, tmp_zip_location)
		with open(zip_file_location, 'w') as out_file:
			out_file.write(base64.b64decode(b64_contents))
		with zipfile.ZipFile(zip_file_location) as in_file:
			in_file.extractall(dest)
		os.remove(zip_file_location)
		with open(os.path.join(dest, CONFIG_FILE), 'w') as config_file:
			config_file.write(json.dumps({"repo-name": path}))
		console.hud_alert(path + ' Downloaded')

	def urlscheme_overwrite_file_with_wc_copy(self, path, b64_contents):
		text = base64.b64decode(b64_contents)
		full_file_path = os.path.join(DOCS_DIR, path)
		try:
			os.makedirs(full_file_path)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise e
		with open(full_file_path, 'w') as f:
			f.write(text)
		editor.open_file(path)
		_, filename = os.path.split(path)
		console.hud_alert(filename + ' Updated')


def main(url_action=None, url_args=None):
	wc = WorkingCopySync()
	if not url_action:
		wc.present()
	elif url_action == 'copy_repo':
		wc.urlscheme_copy_repo_from_wc(url_args[0], url_args[1])
	elif url_action == 'overwrite_file':
		wc.urlscheme_overwrite_file_with_wc_copy(url_args[0], url_args[1])
	elif url_action == 'repo_list':
		wc.copy_repo_from_wc(repo_list=[repo['name'] for repo in json.loads(url_args[0])])
	else:
		msg = "Not a valid URL scheme action. Now say you're sorry."
		console.alert(msg, button1="I'm sorry.", hide_cancel_button=True)

if __name__ == "__main__":
	url_action, url_args = None, None
	if len(sys.argv) > 1:
		url_action = sys.argv[1]
		url_args = sys.argv[2:]
	main(url_action, url_args)
