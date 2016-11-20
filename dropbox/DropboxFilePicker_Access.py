# coding: utf-8

# https://gist.github.com/omz/fb180c58c94526e2c40b

# https://forum.omz-software.com/topic/2729/omz-dropboxfilepicker-synchronous-version

# IMPORTANT SETUP INSTRUCTIONS:
# 
# 1. Go to http://www.dropbox.com/developers/apps (log in if necessary)
# 2. Select "Create App"
# 3. Select the following settings:
#    * "Dropbox API app"
#    * "Files and datastores"
#    * "(No) My app needs access to files already on Dropbox"
#    * "All file types"
#    * (Choose any app name)
# 4. On the newly-created app's summary page, click the "Generate"
#    button under "Generated access token"
# 5. Copy the generated token (a long string of gibberish) and
#    paste it below (replace YOUR_TOKEN_HERE).
# 6. (optional) Open the "wrench" (actions) menu in Pythonista and add
#    this script, so you can run it from everywhere.

# Notes:
# All selected files are downloaded into the root folder of the Pythonista
# script library. If a file with the same name already exists, a numeric
# suffix is appended automatically.

TOKEN = 'nK0yEWMfhNAAAAAAAABACBTmHO44W2rJBt95E2w9LS1kpOyL5mv6eVlDUKHD47xP'

import requests
import urllib
import os
import ui

def list_folder(folder_path='/'):
	headers = {'Authorization': 'Bearer %s' % (TOKEN,)}
	r = requests.get('https://api.dropbox.com/1/metadata/dropbox/%s?list=true' % (urllib.quote(folder_path.encode('utf-8')),), headers=headers)
	result = r.json()
	return result.get('contents', None)
	
def download_file(path, dest_filename, progress=None):
	headers = {'Authorization': 'Bearer %s' % (TOKEN,)}
	url_path = urllib.quote(path.encode('utf-8'))
	url = 'https://api-content.dropbox.com/1/files/dropbox/%s' % (url_path,)
	r = requests.get(url, stream=True, headers=headers)
	dest_path = os.path.join(os.path.expanduser('~/Documents'), dest_filename)
	i = 1
	while os.path.exists(dest_path):
		base, ext = os.path.splitext(dest_filename)
		dest_path = os.path.join(os.path.expanduser('~/Documents'), base + '-' + str(i) + ext)
		i += 1
	size = r.headers.get('Content-Length', 0)
	bytes_written = 0
	canceled = False
	with open(dest_path, 'w') as f:
		for chunk in r.iter_content(1024*10):
			f.write(chunk)
			bytes_written += len(chunk)
			if size > 0 and callable(progress):
				p = float(bytes_written) / float(size)
				should_cancel = progress(p)
				if should_cancel:
					canceled = True
					break
	if canceled:
		os.remove(dest_path)

class DropboxView (ui.View):
	def __init__(self, path='/'):
		tv = ui.TableView()
		tv.frame = self.bounds
		tv.flex = 'WH'
		ds = ui.ListDataSource([])
		ds.action = self.item_selected
		tv.data_source = ds
		tv.delegate = ds
		self.tableview = tv
		self.add_subview(self.tableview)
		self.name = 'Dropbox'
		label = ui.Label(frame=self.bounds)
		label.flex = 'WH'
		label.background_color = (1, 1, 1, 0.95)
		label.text = 'Loading...'
		label.touch_enabled = True
		label.alignment = ui.ALIGN_CENTER
		self.path = path
		self.add_subview(label)
		self.status_label = label
		self.canceled = False
	
	def will_close(self):
		self.canceled = True
	
	def item_selected(self, sender):
		item = sender.items[sender.selected_row]
		if item.get('is_dir', False):
			self.status_label.text = 'Loading Folder...'
			self.status_label.hidden = False
			self.path = item['path']
			self.load_folder()
		elif item.get('up', False):
			self.status_label.text = 'Loading Folder...'
			self.status_label.hidden = False
			self.path = os.path.split(self.path)[0]
			self.load_folder()
		else:
			path = item.get('path')
			self.download_file(path)
	
	@ui.in_background
	def download_file(self, path):
		self.status_label.text = 'Downloading %s...' % (path,)
		self.status_label.hidden = False
		download_file(path, os.path.split(path)[1], self.download_progress)
		self.status_label.hidden = True
	
	def download_progress(self, p):
		self.status_label.text = '%i %% Downloaded...' % (p*100,)
		return self.canceled
	
	@ui.in_background
	def load_folder(self):
		infos = list_folder(self.path)
		items = []
		if self.path != '/':
			items.append({'title': '..', 'image': 'ionicons-arrow-up-c-32', 'up': True})
		if not infos:
			import console
			console.alert('Error', 'Could not load folder. Please check if you entered the access token correctly.', 'OK', hide_cancel_button=True)
			self.status_label.hidden = True
			return
		for info in infos:
			path = info.get('path')
			name = os.path.split(path)[1]
			if name.startswith('.'):
				continue
			is_dir = info.get('is_dir', False)
			item = {'title': name, 'image': 'ionicons-folder-32' if is_dir else 'ionicons-ios7-download-outline-32', 'accessory_type': 'disclosure_indicator' if is_dir else 'none', 'is_dir': is_dir, 'path': info['path']}
			items.append(item)
		def c(o1, o2):
			u_cmp = -1 * cmp(o1.get('up', False), o2.get('up', False))
			if u_cmp != 0:
				return u_cmp
			d_cmp = -1 * cmp(o1.get('is_dir', False), o2.get('is_dir', False))
			if d_cmp == 0:
				return cmp(o1.get('path', '').lower(), o2.get('path', '').lower())
			return d_cmp
		items.sort(cmp=c)
		self.tableview.data_source.items = items
		self.status_label.hidden = True
		self.name = self.path

root_view = DropboxView()
root_view.frame = (0, 0, 500, 500)
root_view.present('sheet')
root_view.load_folder()