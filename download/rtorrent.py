# coding: utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from __future__ import print_function
import ui
import socket
import time
import console
import xmlrpclib
from threading import Timer
from dropbox import client, rest, session

DROPBOX_APP_KEY = 'YOUR DROPBOX APP KEY'
DROPBOX_APP_SECRET = 'YOUR DROPBOX APP SECRET'
RTORRENT_URL = "http://user:password@server"

def activity(fn):
	def activity_fn(*args, **kwargs):
		try:
			console.show_activity()
			fn(*args, **kwargs)
		finally:
			console.hide_activity()
	return activity_fn

class PythonistaDisk(object):
	token_filename = 'rtorrent_dropbox_token.txt'
	def __init__(self, main_view):
		# Get your app key and secret from the Dropbox developer website
		APP_KEY = DROPBOX_APP_KEY
		APP_SECRET = DROPBOX_APP_SECRET
		ACCESS_TYPE = 'app_folder'

		self.main_view = main_view

		sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

		token = self.get_access_token(sess)
		sess.set_token(*token)
		self.client = client.DropboxClient(sess)
		#print "linked account:", self.client.account_info()

	def obtain_access_token(self, sess):
		import webbrowser
		request_token = sess.obtain_request_token()
		url = sess.build_authorize_url(request_token)
		console.alert('Authorization', "Please visit Dropbox website and press the 'Allow' button, then come back.", 'Ok', hide_cancel_button=True)
		webbrowser.open('safari-'+url)
		time.sleep(5)
		while not self.main_view.on_screen:
			time.sleep(1)
		access_token = sess.obtain_access_token(request_token)
		return access_token.key, access_token.secret

	def read_access_token(self):
		with open(self.token_filename, 'r') as f:
			return f.read().strip().split(':')
		
	def get_access_token(self, sess):
		try:
			return self.read_access_token()
		except IOError as e:
			token = self.obtain_access_token(sess)
			with open(self.token_filename, 'w') as f:
				f.write(token[0]+':'+token[1])
				return token

	def search(self, path, query):
		return [ entry['path'] for entry in self.client.search(path, query) ]
		
	def read(self, path):
		return self.client.get_file(path)
		
	def get_url(self, path):
		return self.client.media(path)['url']

	def unlink(self, path):
		try:
			self.client.file_delete(path)
		except dropbox.rest.ErrorResponse:
			pass

class TorrentMgr(object):
	def __init__(self, address):
		self.proxy = xmlrpclib.ServerProxy(RTORRENT_URL)
		self.update()
		
	def update(self):
		self.ids = self.proxy.download_list()
		self.downloads = [self.proxy.d.get_name(i) for i in self.ids]
	
	def get_downloads(self):
		return self.downloads

	def get_name(self, id):
		return self.proxy.d.get_name(id)

	def load(self, torrent_path):
		with open(torrent_path, 'rb') as f:
			data = f.read()
			return self.load_raw(data)
			
	def load_raw(self, torrent_raw):
		#print secure_filename(torrent_raw)
		return self.proxy.load_raw_start(torrent_raw)

	def load_url(self, url):
		print(url)
		print(self.proxy.load_start(url))

	def erase(self, id):
		self.proxy.d.erase(id)
		self.update()
	

class MyView (ui.View):
	def __init__(self, **kwargs):
		screen_sz = ui.get_screen_size()
		self.info = ui.load_view('rtorrent')
		self.info['deleteButton'].action = self.on_delete_clicked
		ui.View.__init__(self, *kwargs)
		
		self.add_view = ui.TableView()
		
		data = ui.ListDataSource([])
		data.action = self.on_row_picked
		data.delete_enabled = False 
		
		tableview = ui.TableView()
		tableview.flex = 'WH'
		tableview.data_source = data
		tableview.delegate = data
		tableview.allows_selection = True 
		data.action = self.on_row_picked
		
		addButton = ui.ButtonItem(title='+')
		addButton.action = self.on_add_torrent_clicked
		addButton.enabled = True 
		
		self.right_button_items = [addButton]
		
		nav = ui.NavigationView(tableview)
		self.add_subview(nav)
		nav.add_subview(tableview)
		nav.flex='TBWH'
		nav.frame = self.bounds

		self.nav = nav
		self.data = data
		
		self.mgr = TorrentMgr('')
		self.update()
		
		self.dropbox = None
		self.torrent_priority = None

	@ui.in_background
	@activity
	def update(self):
		self.mgr.update()
		self.data.items = self.mgr.get_downloads()

	@ui.in_background
	@activity
	def on_torrent_file_picked(self, sender):
		file = sender.items[sender.selected_row]
		self.mgr.load_url(self.dropbox.get_url(file))
		try:
			console.alert('Delete from Dropbox?', '', 'Yes, please')
			time.sleep(5)
			self.dropbox.unlink(file)
		except KeyboardInterrupt:
			time.sleep(5)
		 
		self.update()
		self.nav.pop_view()
	
	@ui.in_background
	@activity
	def on_add_torrent_clicked(self, sender):
		if not self.add_view.on_screen:
			self.dropbox = self.dropbox or PythonistaDisk(self)
			data = ui.ListDataSource([])
			data.action = self.on_torrent_file_picked
			data.delete_enabled = False
			self.add_view.data_source = data
			self.add_view.delegate = data
			self.nav.push_view(self.add_view)
			files = self.dropbox.search('/', '.torrent')
			data.items = files

	@ui.in_background
	@activity
	def update_percents(self, id, size):
		if id == self.picked_id and self.info.on_screen:
			d = self.mgr.proxy.d
			completed = d.get_completed_chunks(id)
			rate = d.get_down_rate(id)
			self.info['completedLabel'].text = '%.2f%% (%.2f kB/sec)' % (100.0*completed/size, rate/1024.0)
			def hash_color(): return 'red' if d.is_hash_checking(id) else 'green'
			def btn_color(): return hash_color() if d.get_complete(id) else 'gray'
			self.info['checkButton'].background_color = btn_color()
			Timer(5, self.update_percents, (id, size)).start()

	def update_info(self, id):
		d = self.mgr.proxy.d
		f = self.mgr.proxy.f
		size = d.get_size_chunks(id)
		self.info['nameLabel'].text = self.mgr.get_name(id)
		self.info['sizeLabel'].text = '%.2f Mb' % (d.get_size_bytes(id)/1024.0/1024.0)
		prio = d.get_priority(id)
		self.show_torrent_priority(prio)
		self.info['prioritySlider'].value = 1.0*prio/3
		files = [ f.get_path(id, n) for n in xrange(d.get_size_files(id)) ]
		data = ui.ListDataSource(files)
		self.info['filesTableView'].delegate = data
		self.info['filesTableView'].data_source = data
		self.info['filesTableView'].reload()
		self.show_pause_button(d.is_active(id))
		self.update_percents(id, size)
	
	@ui.in_background
	@activity
	def delete_torrent(self, id):
		reply = console.alert(title='Delete torrent?', button1='Ok')
		if reply == 1:
			self.mgr.erase(id)
			time.sleep(2)
			self.update()
			self.nav.pop_view()
			self.picked_id = None

	def show_torrent_priority(self, val):
		if val == 0:
			level = 'Off'
		elif val == 1:
			level = 'Low'
		elif val == 2:
			level = 'Normal'
		else:
			level = 'High'

		self.info['priorityLabel'].text = level
		self.torrent_priority = val

	@ui.in_background
	@activity
	def set_torrent_priority(self, val):
		if self.on_screen:
			self.mgr.proxy.d.set_priority(self.picked_id, val)

	def update_torrent_priority(self, val):
		if self.torrent_priority != val:
			self.show_torrent_priority(val)
			self.set_torrent_priority(val)
	
	def on_priority_changed(self, sender):
		val = sender.value
		if val > 2.0/3.0:
			self.update_torrent_priority(3)
		elif val > 1.0/3.0:
			self.update_torrent_priority(2)
		elif val > 0:
			self.update_torrent_priority(1)
		else:
			self.update_torrent_priority(0)

	def show_pause_button(self, is_active):
		text = 'Pause' if is_active else 'Start'
		self.info['pauseButton'].title = text
 
	@ui.in_background
	@activity
	def on_pause_clicked(self, sender):
		d, id = self.mgr.proxy.d, self.picked_id
		is_active = False if sender.title == 'Pause' else True
		self.show_pause_button(is_active)
		d.resume(id) if is_active else d.pause(id)

	@ui.in_background
	@activity
	def on_check_clicked(self, sender):
		if self.mgr.proxy.d.get_complete(self.picked_id):
			self.mgr.proxy.d.check_hash(self.picked_id)

	def on_delete_clicked(self, sender):
		self.delete_torrent(self.picked_id)

	@ui.in_background
	@activity
	def on_row_picked(self, sender):
		self.picked_id = self.mgr.ids[sender.selected_row]
		self.update_info(self.picked_id)
		self.nav.push_view(self.info, True)

v = MyView()
v.present('sheet')
 
