# https://gist.github.com/ywangd/184b9e0e1e76d8b92063

"""
Basic client for Pythonista Script Index (https://github.com/ywangd/Pythonista-Script-Index)

See also: https://github.com/ywangd/psiclient
"""
from __future__ import print_function
import platform
import sys
import os
import urllib2
import json
import collections
import random
import copy
import shutil
import zipfile
import re

import console
import ui


URL_MAIN_INDEX = 'https://raw.githubusercontent.com/ywangd/Pythonista-Script-Index/master/index.json'
SCRIPT_ROOT = os.path.realpath(os.path.abspath(os.path.dirname(__file__)))
RECORD_FILE = os.path.expanduser('~/Documents/.psiclient.json')


class WgetException(Exception):
	pass
class UnzipException(Exception):
	pass
class PsicException(Exception):
	pass
class InvalidGistURLError(Exception):
	pass
class MultipleFilesInGistError(Exception):
	pass
class NoFilesInGistError(Exception):
	pass
class GistDownloadError(Exception):
	pass
	
	
def is_gist(url):
	match = re.match('http(s?)://gist.github.com/([0-9a-zA-Z]*)/([0-9a-f]*)', url)
	return match
	
	
def download_gist(gist_url):
	# Returns a 2-tuple of filename and content
	gist_id_match = re.match('http(s?)://gist.github.com/([0-9a-zA-Z]*)/([0-9a-f]*)', gist_url)
	if gist_id_match:
		import requests
		
		gist_id = gist_id_match.group(3)
		json_url = 'https://api.github.com/gists/' + gist_id
		try:
			gist_json = requests.get(json_url).text
			gist_info = json.loads(gist_json)
			history = gist_info['history']
			nrevisions = len(history)
			files = gist_info['files']
		except:
			raise GistDownloadError()
		py_files = []
		for file_info in files.values():
			lang = file_info.get('language', None)
			if lang != 'Python':
				continue
			py_files.append(file_info)
		if len(py_files) > 1:
			raise MultipleFilesInGistError()
		elif len(py_files) == 0:
			raise NoFilesInGistError()
		else:
			file_info = py_files[0]
			filename = file_info['filename']
			content = file_info['content']
			return filename, content, nrevisions
	else:
		raise InvalidGistURLError()
		
		
def wget(url, output_file=None):
	""" wget: downloads a file from a url """
	
	if not output_file:
		file_name, ext = os.path.splitext(url.split('/')[-1])
		output_file = file_name + ext
	else:
		output_file = output_file
		
	try:
		#console.show_activity()
		u = urllib2.urlopen(url)
		print('Opening: %s' % url)
		
		meta = u.info()
		try:
			file_size = int(meta.getheaders("Content-Length")[0])
		except IndexError:
			file_size = 0
			
		print("Save as: %s " % output_file, end=' ')
		if file_size:
			print("(%s bytes)" % file_size)
		else:
			print()
			
		with open(output_file, 'wb') as f:
			file_size_dl = 0
			block_sz = 8192
			while True:
				buf = u.read(block_sz)
				if not buf:
					break
				file_size_dl += len(buf)
				f.write(buf)
				if file_size:
					status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
				else:
					status = "%10d" % file_size_dl
					
				print(status)
				
	except:
		raise WgetException('not valid url')
		
	finally:
		# console.hide_activity()
		pass
		
		
def unzip(zfile, exdir=None):
	"""Extract a zip archive into a directory."""
	
	files_extracted = []
	
	if not os.path.isfile(zfile):
		raise UnzipException("%s: No such file" % zfile)
		
	else:
		# PK magic marker check
		with open(zfile) as f:
			try:
				pk_check = f.read(2)
			except:
				pk_check = ''
				
		if pk_check != 'PK':
			raise UnzipException("%s: does not appear to be a zip file" % zfile)
			
		if os.path.basename(zfile).lower().endswith('.zip'):
			altpath = os.path.splitext(os.path.basename(zfile))[0]
		else:
			altpath = os.path.basename(zfile) + '_unzipped'
		altpath = os.path.join(os.path.dirname(zfile), altpath)
		location = exdir or altpath
		if (os.path.exists(location)) and not (os.path.isdir(location)):
			print("%s: destination is not a directory" % location)
			sys.exit(1)
		elif not os.path.exists(location):
			os.makedirs(location)
			
		with open(zfile, 'rb') as zipfp:
			try:
				zipf = zipfile.ZipFile(zipfp)
				# check for a leading directory common to all files and remove it
				dirnames = [os.path.join(os.path.dirname(x), '') for x in zipf.namelist()]
				common_dir = os.path.commonprefix(dirnames or ['/'])
				# Check to make sure there aren't 2 or more sub directories with the same prefix
				if not common_dir.endswith('/'):
					common_dir = os.path.join(os.path.dirname(common_dir), '')
				for name in zipf.namelist():
					data = zipf.read(name)
					fn = name
					if common_dir:
						if fn.startswith(common_dir):
							fn = fn.split(common_dir, 1)[-1]
						elif fn.startswith('/' + common_dir):
							fn = fn.split('/' + common_dir, 1)[-1]
					fn = fn.lstrip('/')
					fn = os.path.join(location, fn)
					dirf = os.path.dirname(fn)
					
					if not os.path.exists(dirf):
						os.makedirs(dirf)
						
					if fn.endswith('/'):  # A directory
						if not os.path.exists(fn):
							os.makedirs(fn)
					else:
						fp = open(fn, 'wb')
						try:
							fp.write(data)
						finally:
							fp.close()
							
					files_extracted.append(fn)
					
			except:
				raise UnzipException("%s: zip file is corrupt" % zfile)
				
	return files_extracted
	
	
def top_dir(path):
	dirname = os.path.dirname(path)
	if dirname == '':
		return path
	else:
		return top_dir(dirname)
		
		
def refreshable_url(url):
	return '%s?q=%d' % (url, random.randint(0, 99999))
	
	
def dict_update(d, u):
	for k, v in u.iteritems():
		if isinstance(v, collections.Mapping):
			r = dict_update(d.get(k, {}), v)
			d[k] = r
		else:
			d[k] = u[k]
	return d
	
	
def get_release_for_version(releases, ver_num=None):
	if ver_num is not None:
		print(repr(ver_num))
		print(repr(releases))
		for release in releases:
			if ver_num == release['version']:
				return release
	else:
		ver_digits = (0, 0, 0)
		target_release = None
		try:
			for release in releases:
				if release['version'] is None:
					raise KeyError()
				this_ver_digits = map(int, release['version'].split('.'))
				if len(this_ver_digits) < 3:
					this_ver_digits += (0,) * (3 - len(this_ver_digits))
				for i, digit in enumerate(this_ver_digits):
					if ver_digits[i] < digit:
						ver_digits = this_ver_digits
						target_release = release
			return target_release
		except KeyError:  # if no version info, just return the first release
			if releases:
				release = releases[0]
				release['version'] = None
				return release
	return None
	
	
class MergedIndices(object):

	def __init__(self, remote_index_url, record_file, load_remote=True, dest_dir=None):
		self.remote_index_url = remote_index_url
		self.record_file = record_file
		self.dest_dir = os.path.expanduser(dest_dir) if dest_dir \
		else os.path.join(os.environ['HOME'], 'Documents/bin')
		
		if not os.path.exists(self.dest_dir) or not os.path.isdir(self.dest_dir):
			os.mkdir(self.dest_dir)
			
		if load_remote:
			self.remote_index = self.load_remote_index()
		else:
			self.remote_index = {'scripts': {}}
			
		self.local_indices = self.load_local_record()
		
		self.merged_indices = None
		self.merged_index = None
		self.merge_remote_and_local()
		
	def load_local_record(self):
		if not os.path.exists(self.record_file):
			with open(self.record_file, 'w') as outs:
				outs.write('{}')
			return {}
		else:
			with open(self.record_file) as ins:
				return json.load(ins)
				
	def load_remote_index(self):
		return json.loads(urllib2.urlopen(refreshable_url(self.remote_index_url)).read())
		
	def merge_remote_and_local(self):
		self.merged_indices = {self.remote_index_url: copy.deepcopy(self.remote_index)}
		dict_update(self.merged_indices, copy.deepcopy(self.local_indices))
		self.merged_index = self.merged_indices[self.remote_index_url]
		
	def save_local_record(self):
		with open(self.record_file, 'w') as outs:
			json.dump(self.local_indices, outs, indent=1)
			
	def do_list(self):
		script_list = []
		for url in sorted(self.merged_indices.keys()):
			index = self.merged_indices[url]
			scripts = index['scripts']
			for script_name in sorted(scripts.keys()):
				entry = scripts[script_name]
				installed = entry.get('installed', None)
				description = entry.get('description', None)
				script_list.append({"short_name": script_name,
				"description": description,
				"installed": installed})
		return script_list
		
	def do_install(self, script_name, ver_num=None, dest_dir=None):
		if script_name not in self.merged_index['scripts'].keys():
			raise PsicException('%s: not found' % script_name)
			
		elif self.merged_index['scripts'][script_name].get('installed', None):
			raise PsicException('%s: already installed' % script_name)
			
		else:
			meta_url, tag = urllib2.splittag(self.merged_index['scripts'][script_name]['meta_url'])
			jmsg = json.loads(urllib2.urlopen(refreshable_url(meta_url)).read())
			jmsg = jmsg[tag] if tag else jmsg
			
			releases = jmsg['releases']
			
			release = get_release_for_version(releases, ver_num)
			if release is None:
				raise PsicException('%s: release not found' % script_name)
				
			if 'filetype' not in release:
				if release['url'].endswith('.py') or is_gist(release['url']):
					release['filetype'] = 'SingleFile'
				elif release['url'].endswith('.zip'):
					release['filetype'] = 'ZippedFiles'
				else:
					raise PsicException('%s: unknown filetype' % script_name)
					
			if not dest_dir:
				dest_dir = self.dest_dir
			else:
				dest_dir = os.path.expanduser(dest_dir)
				
			dest_dir = os.path.abspath(dest_dir)
			if not os.path.exists(dest_dir) or not os.path.isdir(dest_dir):
				os.makedirs(dest_dir)
				
			filetype = release['filetype']
			files_installed = []
			
			full_name = jmsg.get('name', None)
			if full_name is None:
				full_name = script_name
				
			saved_dir = os.getcwd()
			try:
				if filetype == 'SingleFile':
					os.chdir(dest_dir)
					filename = full_name if full_name.endswith('.py') else (full_name + '.py')
					if release['url'].endswith('.py'):
						wget(release['url'], output_file=filename)
						files_installed.append(filename)
						raw_match = re.match('http(s?)://raw.github.com/gist/', release['url'])
						raw_match2 = re.match('http(s?)://gist.githubusercontent.com/([0-9a-zA-Z]*)/([0-9a-f]*)/raw/', release['url'])
						if not raw_match and not raw_match2:
							try:
								filename_pyui = filename + 'ui'
								wget(release['url'] + 'ui', output_file=filename_pyui)
								files_installed.append(filename_pyui)
							except WgetException:
								pass
					elif is_gist(release['url']):
						try:
							_, content, nrevisions = download_gist(release['url'])
						except (InvalidGistURLError, MultipleFilesInGistError, NoFilesInGistError, GistDownloadError):
							raise PsicException('%s: Gist url error' % release['url'])
						with open(filename, 'w') as outs:
							outs.write(content)
						files_installed.append(filename)
						if release['version'] is None:
							release['version'] = '%d.0.0' % nrevisions
					else:
						raise PsicException('%s: invalid single file url' % release['url'])
						
				elif filetype == 'ZippedFiles':
					os.chdir(os.environ['TMPDIR'])
					wget(release['url'], output_file='files.zip')
					this_dest_dir = os.path.join(dest_dir, full_name)
					if not os.path.exists(this_dest_dir) or not os.path.isdir(this_dest_dir):
						os.mkdir(this_dest_dir)
					files_extracted = unzip('files.zip', exdir=this_dest_dir)
					for f in files_extracted:
						if f.strip() == '':
							continue
						f = os.path.relpath(f, dest_dir)
						if f != '.':
							files_installed.append(f)
					os.remove('files.zip')
				else:
					raise PsicException('%s: unknown filetype' % script_name)
					
			finally:
				os.chdir(saved_dir)
				
			installed = {
			'version': release['version'],
			'dest_dir': dest_dir,
			'filetype': release['filetype'],
			'files': files_installed
			}
			
			if self.remote_index_url not in self.local_indices:
				self.local_indices[self.remote_index_url] = {'scripts': {}}
				
			self.local_indices[self.remote_index_url]['scripts'][script_name] = {'installed': installed}
			self.save_local_record()
			self.merge_remote_and_local()
			return script_name, installed
			
	def do_remove(self, script_name):
		if script_name not in self.remote_index['scripts'].keys():
			raise PsicException('%s: script not found' % script_name)
			
		else:
			entry = self.merged_index['scripts'][script_name]
			if entry.get('installed', None) is None:
				raise PsicException('%s: script not installed' % script_name)
				
			saved_dir = os.getcwd()
			try:
				os.chdir(entry['installed']['dest_dir'])
				if entry['installed']['filetype'] == 'SingleFile':
					for f in entry['installed']['files']:
						os.remove(f)
				elif entry['installed']['filetype'] == 'ZippedFiles':
					removed_dirs = set()
					for f in entry['installed']['files']:
						this_dir = os.path.dirname(f)
						if this_dir in removed_dirs or top_dir(this_dir) in removed_dirs:
							continue
						if this_dir != '' and this_dir not in removed_dirs:
							shutil.rmtree(this_dir)
							removed_dirs.add(this_dir)
						elif os.path.isdir(f):
							shutil.rmtree(f)
							removed_dirs.add(f)
						else:
							os.remove(f)
							
			finally:
				os.chdir(saved_dir)
				
			self.local_indices[self.remote_index_url]['scripts'].pop(script_name)
			self.save_local_record()
			self.merge_remote_and_local()
			return script_name
			
	def do_info(self, script_name):
		if script_name not in self.remote_index['scripts'].keys():
			raise PsicException('%s: script not found' % script_name)
			
		else:
			entry = self.remote_index['scripts'][script_name]
			if 'info' in entry.keys():
				return script_name, entry['info'], self.merged_index['scripts'][script_name].get('installed', None)
				
			meta_url, tag = urllib2.splittag(self.remote_index['scripts'][script_name]['meta_url'])
			jmsg = json.loads(urllib2.urlopen(refreshable_url(meta_url)).read())
			jmsg = jmsg[tag] if tag else jmsg
			
			jmsg['author'] = jmsg.get('author', '')
			jmsg['email'] = jmsg.get('email', '')
			jmsg['website'] = jmsg.get('website', '')
			jmsg['long_description'] = jmsg.get('long_description', 'N/A')
			jmsg['releases'] = jmsg.get('releases', [])
			
			releases = []
			for release in jmsg.get('releases', []):
				release['version'] = release.get('version', None)
				releases.append(release)
				
			jmsg['releases'] = releases
			
			self.remote_index['scripts'][script_name]['info'] = jmsg
			
			installed = self.merged_index['scripts'][script_name].get('installed', None)
			
			return script_name, jmsg, installed
			
			
info_templ = r"""%s

Author: %s
Email: %s
Website: %s
Status:
    %s
    %s
"""

alert_duration = 1.0


if __name__ == '__main__':

	_ON_IPAD = platform.machine().startswith('iPad')
	
	desc_page = ui.View(flex='WH')
	desc_page.background_color = 0.8
	desc_tv = ui.TextView(flex='W')
	desc_page.add_subview(desc_tv)
	desc_tv.editable = False
	desc_tv.font = ('AppleSDGothicNeo-Regular', 16)
	desc_tv.border_width = 1
	
	
	psiclient = ui.View(flex='WH')
	psiclient.background_color = 'white'
	psiclient.name = 'Pythonista Script Index'
	
	psitable = ui.TableView(flex='WH')
	
	listsource = ui.ListDataSource(['Loading ...'])
	listsource.delete_enabled = False
	psitable.data_source = listsource
	psitable.delegate = listsource
	
	psiclient.add_subview(psitable)
	
	nav_view = ui.NavigationView(psiclient)
	nav_view.name = 'psiclient'
	
	if _ON_IPAD:
		psitable.width = 540
		psitable.height = 575
	else:
		psitable.width, psitable.height = ui.get_screen_size()
	height_nudge = 110
	psitable.height -= height_nudge
	
	if _ON_IPAD:
		nav_view.present('sheet')
	else:
		nav_view.present('fullscreen')
		
	merged_indices = MergedIndices(URL_MAIN_INDEX, RECORD_FILE, dest_dir='~/Documents/bin')
	item_content = {}
	
	def make_items():
		items = []
		for item in merged_indices.do_list():
			items.append({'title': '%s (%s)' % (item['short_name'], 'installed' if item['installed'] else 'available'),
			'accessory_type': 'disclosure_indicator',
			'short_name': item['short_name'],
			'description': item.get('description', 'No description'),
			'installed': item['installed']})
		return items
		
	def make_button(title, action):
		btn = ui.Button(name='btn', title=' %s ' % title)
		btn.background_color = 'white'
		btn.tint_color = 'black'
		btn.border_width = 1
		btn.corner_radius = 5
		btn.font = (btn.font[0], 18)
		btn.action = action
		btn.size_to_fit()
		btn.x = (desc_page.width - btn.width) / 2
		btn.y = 320
		return btn
		
	def make_info_page_texts():
		info = item_content['info']
		installed = item_content['installed']
		release = get_release_for_version(info['releases'])
		description = info['long_description'] if info['long_description'] else item_content['description']
		rl_ver = release['version'] if release['version'] else 'N/A'
		if installed:
			lc_ver = installed['version'] if installed['version'] else 'N/A'
			
		desc_tv.text = info_templ % (description,
		info['author'],
		info['email'],
		info['website'],
		'available (version: %s)' % rl_ver,
		('installed (version: %s)' % lc_ver) if installed else '')
		
	def install_action(sender):
		try:
			short_name = item_content['short_name']
			merged_indices.do_install(short_name)
			console.hud_alert('success', 'success', alert_duration)
			
			listsource.items = make_items()
			item_content['installed'] = merged_indices.merged_index['scripts'][short_name]['installed']
			btn = make_button('Uninstall', remove_action)
			sender.superview.add_subview(btn)
			sender.superview.remove_subview(sender)
			make_info_page_texts()
			
		except:
			console.hud_alert('failed', 'error', alert_duration)
			
	def remove_action(sender):
		try:
			short_name = item_content['short_name']
			merged_indices.do_remove(short_name)
			console.hud_alert('success', 'success', alert_duration)
			
			listsource.items = make_items()
			item_content['installed'] = None
			btn = make_button('Install', install_action)
			sender.superview.add_subview(btn)
			sender.superview.remove_subview(sender)
			make_info_page_texts()
			
		except:
			console.hud_alert('failed', 'error', alert_duration)
			
	@ui.in_background
	def info_action():
		_, info, installed = merged_indices.do_info(item_content['short_name'])
		item_content['info'] = info
		item_content['installed'] = installed
		make_info_page_texts()
		if installed:
			btn = make_button('Uninstall', remove_action)
			desc_page.add_subview(btn)
			
		else:
			btn = make_button('Install', install_action)
			desc_page.add_subview(btn)
			
	def list_item_tapped(sender):
		item_content.clear()
		row_item = sender.items[sender.selected_row]
		item_content['short_name'] = row_item['short_name']
		item_content['description'] = row_item['description']
		desc_page.name = row_item['short_name']
		desc_tv.height = 300 # desc_page.height / 2
		desc_tv.text = 'Loading ...'
		psiclient.navigation_view.push_view(desc_page)
		
		for sv in desc_page.subviews:
			if sv.name == 'btn':
				desc_page.remove_subview(sv)
				
		info_action()
		
	listsource.items = make_items()
	
	listsource.action = list_item_tapped

