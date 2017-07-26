#!/usr/bin/env python2
#coding: utf-8

# https://github.com/nekotaroneko/CleverSFTPClient

# https://forum.omz-software.com/topic/3712/share-cleversftpclient

import ui, os, threading,console
import editor
import time
import shutil
from core.Utilities import *
import core.configparser as configparser
import core.uicomponents.uidir as uidir
import logging
import dialogs
import traceback
import speech
from datetime import datetime, timedelta
import json

class CleverSFTPClient(ui.View):

	def __init__(self):
		self.config = configparser.ConfigParser()
		if not os.path.exists(config_path):
			self.config.write(open(config_path, 'w'))
		self.config.read(config_path)
		
		self.remoteFile = ''
		self.connect = False
		self.sftp = None
		self.local_dirname = app_root_path
		self.remote_list = []
		self.busy = False
		
		
		if os.path.exists(temp_path):
			shutil.rmtree(temp_path)
			os.makedirs(temp_path)
		else:
			os.makedirs(temp_path)
			
		if not os.path.exists(download_path):
			os.makedirs(download_path)
			
		if ui.get_screen_size()[0]+ui.get_screen_size()[1] > 1500:
			view_pyui = 'CleverSFTPClient_iPad'
		else:
			view_pyui = 'CleverSFTPClient_iPhone'
		self.view = ui.load_view(os.path.join(pyui_path, view_pyui))
		self.view['bt_connect'].action = self.bt_connect
		self.view['bt_upload'].action = self.bt_upload
		self.view['bt_download'].action = self.bt_download
		self.view['bt_local_rename'].action = self.bt_local_rename
		self.view['bt_local_delete'].action = self.bt_local_delete
		self.view['bt_local_mkdir'].action = self.bt_local_mkdir
		self.view['bt_remote_rename'].action = self.bt_remote_rename
		self.view['bt_remote_delete'].action = self.bt_remote_delete
		self.view['bt_remote_mkdir'].action = self.bt_remote_mkdir
		self.view['bt_ssh'].action = self.bt_ssh
		self.view['bt_progress'].action = self.bt_progress
		self.view['bt_local_edit'].action = self.bt_local_edit
		self.view['bt_remote_edit'].action = self.bt_remote_edit
		self.view['bt_close'].action = self.bt_close
		self.view['bt_history'].action = self.bt_hostory
		self.view['bt_setting'].action = self.bt_setting
		self.view['sc_passkey'].action = self.sc_passkey
		self.view['bt_remote_chmod'].action = self.bt_remote_chmod
		self.view['bt_remote_favorite'].action = self.bt_remote_favorite
		
		self.view['bt_local_delete'].enabled = False
		self.view['bt_remote_delete'].enabled = False
		self.view['bt_upload'].enabled = False
		self.view['bt_download'].enabled = False
		self.view['bt_local_rename'].enabled = False
		self.view['bt_remote_chmod'].enabled = False
		
		for tf in ['tf_host', 'tf_user', 'tf_passkey']:
			self.view[tf].delegate = self.TextFieldDelegate
			self.view[tf].delegate.textfield_did_change = self.textfield_did_change
			self.view[tf].delegate.textfield_did_begin_editing = self.textfield_did_begin_editing
			
		self.view['bt_connect'].enabled = self.view['bt_ssh'].enabled = False
		
		
		self.view['lb_local'].text = to_relpath(self.local_dirname)
		
		self.tv_local = self.view['tv_local']
		self.tv_remote = self.view['tv_remote']
		self.tv_local_selectable = False
		self.tv_remote_selectable = False
		self.tv_info = Color_Text_View(self.view['tv_info'].frame,auto_scroll=True,editable=False,selectable=True)
		self.tv_info.flex = self.view['tv_info'].flex
		self.view['tv_info'].hidden = True
		self.view.add_subview(self.tv_info)
		#self.remotePath = '/var/' + self.view['tf_user'].text
		self.progress_view = ui.load_view(os.path.join(pyui_path, 'progress'))
		self.progress_view.name = 'Progress View'
		
		self.tv_progress = self.progress_view['tv_progress']
		self.tv_progress.data_source.tableview_cell_for_row = self.progress_tableview_cell_for_row
		self.tv_progress.delegate.tableview_did_select = self.progress_tableview_did_select
		#self.view.add_subview(self.progress_view)
		#self.progress_view.hidden = True
		self.progress_cell_dict = {}
		self.progress_list = []
		
		self.setting_view = ui.load_view(os.path.join(pyui_path, 'setting'))
		self.setting_view['sw_autoscan'].action = self.sw_autoscan
		self.setting_view['sc_log_level'].action = self.sc_log_level
		
		self.favorite_view = ui.load_view(os.path.join(pyui_path, 'favorite'))
		self.favorite_view['bt_add_favorite'].action = self.bt_add_favorite
		self.favorite_view['tv_favorite'].delegate.tableview_did_select = self.favorite_tableview_did_select
		
		self.log = logging.getLogger()
		out_hdlr = logging.StreamHandler(self.tv_info)
		out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
		#out_hdlr.setLevel(logging.INFO)#DEBUG)
		self.log.addHandler(out_hdlr)
		
		if 'system' in self.config:
			if self.config['system']['log_level'] == 'INFO':
				level = logging.INFO
				self.setting_view['sc_log_level'].selected_index = 0
			elif self.config['system']['log_level'] == 'DEBUG':
				level = logging.DEBUG
				self.setting_view['sc_log_level'].selected_index = 1
		else:
			self.config['system'] = {'autoscan':'True', 'log_level':'INFO'}
			self.setting_view['sc_log_level'].selected_index = 0
			level = logging.INFO
		self.log.setLevel(level)
		
		autoscan = self.setting_view['sw_autoscan'].value = self.config['system'].getboolean('autoscan')
		
		self.view['tf_passkey'].clear_button_mode = 'while_editing'
		self.sc_passkey(None)
		
		self.view.present(hide_title_bar=True, orientations=['landscape'])
		
		self.refresh_local_list()
		
		self.stash = None
		
		if autoscan:
			ip = self.find_ssh_server(22)
			if ip:
				if ip in self.config:
					self.set_user_data(ip)
					self.bt_connect(self.view['bt_connect'])
				else:
					self.make_new_host(ip)
					
		else:
			if not len([x for x in self.config.sections() if 'user' in self.config[x]]) == 0:
				self.bt_hostory('')
				
	def bt_add_favorite(self, sender):
		if self.connect:
			full_path = self.remotePath
			title = console.input_alert('CleverSFTPClient', 'Title {}'.format(full_path), '', 'OK')
			favorite_dict = json.loads(self.config[self.host]['favorite'])
			favorite_dict[title] = full_path
			favorite_dict_str = json.dumps(favorite_dict)
			self.config[self.host]['favorite'] = favorite_dict_str
			self.config.write(open(config_path, 'w'))
			self.set_user_data(self.host)
			
				
	def favorite_tableview_did_select(self, tableview, section, row):
		lst = tableview.data_source
		text = lst.items[row]
		lst.selected_row = row
		if lst.action:
			lst.action(lst)
		if self.connect:		
			full_path = self.favorite_dict[text]
			self.remotePath = full_path
			self.refresh_remote_list()
			self.favorite_view.close()
	
	def bt_remote_favorite(self, sender):
		if self.connect:
			self.set_user_data(self.host)
			self.favorite_view.present('sheet')
		
	def close_keyboard(self):
		for tf in ['tf_host', 'tf_user', 'tf_passkey']:
			self.view[tf].end_editing()
			
	def textfield_did_begin_editing(self, textfield):
		if textfield.name == 'tf_passkey':
			if self.pass_or_key == 'key':
				key = uidir.getFile(base_dir=app_root_path)
				if key:
					self.view['tf_passkey'].text = key
					self.view['tf_passkey'].secure = False
					self.pass_or_key = 'key'
				else:
					self.view['sc_passkey'].selected_index = 0
					self.view['tf_passkey'].secure = True
					self.pass_or_key = 'pass'
					
				self.check_connect_ssh_btn_enabled()
				
	def sc_log_level(self, sender):
		segment = self.setting_view['sc_log_level'].segments[self.setting_view['sc_log_level'].selected_index]
		if segment == 'INFO':
			if not self.config['system']['log_level'] == 'INFO':
				self.config['system']['log_level'] = 'INFO'
				self.config.write(open(config_path, 'w'))
			level = logging.INFO
		elif segment == 'DEBUG':
			if not self.config['system']['log_level'] == 'DEBUG':
				self.config['system']['log_level'] = 'DEBUG'
				self.config.write(open(config_path, 'w'))
			level = logging.DEBUG
		self.log.setLevel(level)
				
	def make_new_host(self, ip):
		name = console.input_alert('CleverSFTPClient', 'Display name of {}'.format(ip), '', 'OK', hide_cancel_button=True)
		self.config[ip] = {'name':name, 'favorite':{}}
		self.config.write(open(config_path, 'w'))
		self.view['tf_host'].text = ip
		if self.view['tf_user'].text == '':
			self.view['tf_user'].begin_editing()
		
	class TextFieldDelegate():
		pass
		
	def textfield_did_change(self, textfield):
		self.check_connect_ssh_btn_enabled()
		
	def check_connect_ssh_btn_enabled(self):
		host = self.view['tf_host'].text
		user = self.view['tf_user'].text
		passkey = self.view['tf_passkey'].text
		
		if host == '' or user == '' or passkey == '':
			self.view['bt_connect'].enabled = self.view['bt_ssh'].enabled = False
		else:
			self.view['bt_connect'].enabled = self.view['bt_ssh'].enabled = True
			
	def sc_passkey(self, sender):
		segment = self.view['sc_passkey'].segments[self.view['sc_passkey'].selected_index]
		
		if segment == 'Key' and not sender == None:
			key = uidir.getFile(base_dir=app_root_path)
			if key:
				self.view['tf_passkey'].text = key
				self.view['tf_passkey'].secure = False
				self.pass_or_key = 'key'
			else:
				self.view['sc_passkey'].selected_index = 0
				self.view['tf_passkey'].secure = True
				self.pass_or_key = 'pass'
				
			self.check_connect_ssh_btn_enabled()
			return
			
		ip = self.view['tf_host'].text
		
		if segment == 'Pass':
			self.view['tf_passkey'].secure = True
			self.pass_or_key = 'pass'
			if not sender == None:
			
				if ip in self.config.sections():
					if 'password' in self.config[ip]:
						self.view['tf_passkey'].text = self.config[ip]['password']
					else:
						self.view['tf_passkey'].text = ''
						
					self.view['sc_passkey'].selected_index = 0
					
		elif segment == 'Key':
			self.view['tf_passkey'].secure = False
			self.pass_or_key = 'key'
			if not sender == None:
				if ip in self.config.sections():
					if 'key' in self.config[ip]:
						self.view['tf_passkey'].text = self.config[ip]['key']
					else:
						self.view['tf_passkey'].text = ''
					self.view['sc_passkey'].selected_index = 1
					
		self.check_connect_ssh_btn_enabled()
		
	def sw_autoscan(self, sender):
		self.config['system']['autoscan'] = str(sender.value)
		self.config.write(open(config_path, 'w'))
		
	def bt_setting(self, sender):
		self.setting_view.present('sheet')
		
	def bt_hostory(self, sender):
		ip_dict = {}
		ip_list = []
		for ip in self.config.sections():
			if 'user' in self.config[ip]:
				user = self.config[ip]['user']
				if 'name' in self.config[ip]:
					name = self.config[ip]['name']
					text = 'Name : {} | IP : {} | User : {}'.format(name, ip, user)
				else:
					text = 'IP : {} | User : {}'.format(ip, user)
				ip_dict[text] = ip
				ip_list.append(text)
		_ip = dialogs.list_dialog('History', ip_list)
		if _ip:
			ip = ip_dict[_ip]
			self.set_user_data(ip)
			
			if self.connect:
				self.bt_connect(self.view['bt_connect']) #disconnect
			self.bt_connect(self.view['bt_connect'])
			
	def set_user_data(self, ip):
		self.view['tf_host'].text = ip
		if ip in self.config:
			if 'user' in self.config[ip]:
				self.view['tf_user'].text = self.config[ip]['user']
			else:
				self.view['tf_user'].begin_editing()
				
			if 'password' in self.config[ip]:
				self.view['tf_passkey'].text = self.config[ip]['password']
				self.view['sc_passkey'].selected_index = 0
			elif 'key' in self.config[ip]:
				self.view['tf_passkey'].text = self.config[ip]['key']
				self.view['sc_passkey'].selected_index = 1
				
			if 'favorite' in self.config[ip]:
				favorite_dict =  json.loads(self.config[ip]['favorite'])
				self.favorite_dict = {}
				items = []
				for basename, full_path in favorite_dict.iteritems():
					text = 'Title : {} | Path : {}'.format(basename, full_path)
					items.append(text)
					self.favorite_dict[text] =full_path
				self.favorite_view['tv_favorite'].data_source.items = items
				
			self.sc_passkey(None)
			
			
	def find_ssh_server(self, port):
		port_scan = Port_Scan(port, show_ip=False, alert=True)
		result = port_scan.scan()
		if len(result) == 0:
			return False
		elif len(result) == 1:
			return result[0]
		else:
			ip_dict = {}
			ip_list = []
			text = ''
			for ip in result:
				if ip in self.config:
					config = self.config[ip] 
					if 'name' in config and not config['name'] == '':
						name = config['name']
						text = 'Name : {} | IP : {}'.format(name, ip)
						if 'user' in config and not config['user'] == '':
							user = config['user']
							text += ' | User : {}'.format(user)					
					ip_dict[text] = ip
					ip_list.append(text)
				else:
					text = '{} ##first time##'.format(ip)
					ip_dict[text] = ip
					ip_list.append(text)
			_ip = dialogs.list_dialog('Port 22', ip_list)
			if _ip:
				ip = ip_dict[_ip]
				return ip
			else:
				return False
				
	def bt_close(self, sender):
		try: #for multi run
			self.will_close()
		except:
			pass
		self.view.close()
		
	def will_close(self): #dummy
		if self.connect:
			self.bt_connect(None)
			#self.stash.user_action_proxy.vk_tapped( self.stash.ui.k_CD )
			
		if os.path.exists(temp_path):
			shutil.rmtree(temp_path)
			
			
			
	def bt_local_edit(self, sender):
		if self.tv_local.editing:
			self.tv_local.editing = False
		else:
			self.tv_local.editing = True
			if self.tv_remote.editing:
				self.tv_remote.editing = False
				
		self.tv_local.reload_data()
		self.check_enabled_btn()
		
		
	def bt_remote_edit(self, sender):
		if self.tv_remote.editing:
			self.tv_remote.editing = False
		else:
			self.tv_remote.editing = True
			if self.tv_local.editing:
				self.tv_local.editing = False
		self.tv_remote.reload_data()
		self.check_enabled_btn()
		
	def bt_progress(self, sender):
		self.progress_view.present('sheet')
		'''if self.progress_view.hidden:
		self.progress_view.hidden = False
		else:
		self.progress_view.hidden = True'''
		
	def bt_ssh(self, sender):
		if self.connect:
			if self.stash and not sender == None:
				self.stash.ui.present()
				self.stash.terminal.begin_editing()
				
				
				
				
	def bt_local_rename(self, sender):
		local_file_list =  get_table_list(self.tv_local)[0]
		local_dict = self.local_dict[local_file_list]
		full_path = local_dict['full_path']
		basename = os.path.basename(full_path)
		self.view_po = ui.load_view(os.path.join(pyui_path, os.path.join(pyui_path, 'popover')))
		self.view_po.name = 'Rename'
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['lb_old_name'].text = basename
		self.view_po['tf_new_name'].text = basename
		self.view_po['bt_okay'].action = self.bt_local_rename_okay
		self.view_po['bt_cancel'].action = self.bt_cancel
		
	def bt_local_rename_okay(self, sender):
		local_file_list =  get_table_list(self.tv_local)[0]
		local_dict = self.local_dict[local_file_list]
		full_path = local_dict['full_path']
		to_path = os.path.join(os.path.dirname(full_path), self.view_po['tf_new_name'].text)
		os.rename(full_path, to_path)
		self.view_po.close()
		self.refresh_local_list()
		
		logging.info('color:red rename {} to {}'.format(os.path.basename(full_path), os.path.join(to_path)))
		
		
	def bt_cancel(self, sender):
		self.view_po.close()
		
	def bt_local_delete(self, sender):
		local_file_list =  get_table_list(self.tv_local)
		
		self.view_po = ui.load_view(os.path.join(pyui_path, 'popover'))
		self.view_po.name = 'Delete'
		self.view_po['tf_new_name'].hidden = True
		self.view_po['lb_nn'].hidden = True
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['lb_on'].text = 'Delete:'
		self.view_po['lb_old_name'].text = '\n'.join(local_file_list)
		self.view_po['bt_cancel'].action = self.bt_cancel
		self.view_po['bt_okay'].action = self.bt_local_delete_okay
		
	def bt_local_delete_okay(self, sender, files=None):
		if sender == None:
			file_list = files
		else:
			file_list = get_table_list(self.tv_local)
		for local_file in file_list:
			local_dict = self.local_dict[local_file]
			full_path = local_dict['full_path']
			logging.info('color:red remove({})'.format(full_path))
			if local_dict['type'] == 'dir':
				shutil.rmtree(full_path)
			else:
				os.remove(full_path)
		if not sender == None:
			self.view_po.close()
		self.refresh_local_list()
		
		
	def bt_local_mkdir(self, sender):
		self.view_po = ui.load_view(os.path.join(pyui_path, 'popover'))
		self.view_po.name = 'Make Directory'
		self.view_po['lb_old_name'].hidden = True
		self.view_po['lb_on'].hidden = True
		self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
		self.view_po['lb_nn'].text = 'New Dir:'
		self.view_po['bt_cancel'].action = self.bt_cancel
		self.view_po['bt_okay'].action = self.bt_local_mkdir_okay
		
	def bt_local_mkdir_okay(self, sender):
		directory = self.view_po['tf_new_name'].text
		
		os.mkdir(os.path.join(self.local_dirname, directory))
		self.view_po.close()
		self.refresh_local_list()
		
		logging.info('color:green mkdir {}'.format(directory))
		
		
	def bt_remote_rename(self, sender):
		if self.connect:
			remote_file_list =  get_table_list(self.tv_remote)[0]
			remote_dict = self.remote_dict[remote_file_list]
			full_path = remote_dict['full_path']
			basename = os.path.basename(full_path)
			self.view_po = ui.load_view(os.path.join(pyui_path, 'popover'))
			self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
			self.view_po['lb_old_name'].text = basename
			self.view_po['tf_new_name'].text = basename
			self.view_po['bt_okay'].action = self.bt_remote_rename_okay
			self.view_po['bt_cancel'].action = self.bt_cancel
			
	def bt_remote_rename_okay(self, sender):
		'''ディレクトリが変わるごとにcdしてるのでフルパスの必要はないフルパスだと逆にエラーが出る可能性がある'''
		remote_file_list =  get_table_list(self.tv_remote)[0]
		remote_dict = self.remote_dict[remote_file_list]
		full_path = remote_dict['full_path']
		basename = os.path.basename(full_path)
		
		self.sftp.rename(basename, self.view_po['tf_new_name'].text)
		self.view_po.close()
		self.refresh_remote_list()
		
		logging.info('color:red rename {} to {}'.format(basename, self.view_po['tf_new_name'].text))
		
		
	def bt_remote_delete(self, sender):
		if self.connect:
			remote_file_list =  get_table_list(self.tv_remote)
			
			self.view_po = ui.load_view(os.path.join(pyui_path, 'popover'))
			self.view_po.name = 'Delete'
			self.view_po['tf_new_name'].hidden = True
			self.view_po['lb_nn'].hidden = True
			self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
			self.view_po['lb_on'].text = 'Delete:'
			self.view_po['lb_old_name'].text = '\n'.join(remote_file_list)
			self.view_po['bt_cancel'].action = self.bt_cancel
			self.view_po['bt_okay'].action = self.bt_remote_delete_okay
			
	def bt_remote_delete_okay(self, sender, files=None):
		if sender == None:
			file_list = files
		else:
			file_list = get_table_list(self.tv_remote)
		
		for remote_file in file_list:
			remote_dict = self.remote_dict[remote_file]
			full_path = remote_dict['full_path']
			basename = remote_file

			logging.info('color:red remove({})'.format(full_path))
			try:
				self.sftp.remove(remote_file)
			except IOError:
				#dir
				rmtree(self.sftp, basename)
		if not sender == None:
			self.view_po.close()
		self.refresh_remote_list()
		
		
	def bt_remote_mkdir(self, sender):
		if self.connect:
			self.view_po = ui.load_view(os.path.join(pyui_path, 'popover'))
			self.view_po.name = 'Make Directory'
			self.view_po['lb_old_name'].hidden = True
			self.view_po['lb_on'].hidden = True
			self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
			self.view_po['lb_nn'].text = 'New Dir:'
			self.view_po['bt_cancel'].action = self.bt_cancel
			self.view_po['bt_okay'].action = self.bt_remote_mkdir_okay
			
	def bt_remote_mkdir_okay(self, sender):
		directory = self.view_po['tf_new_name'].text
		
		self.sftp.mkdir(os.path.join(self.remotePath, directory))
		self.view_po.close()
		self.refresh_remote_list()
		
		logging.info('color:green mkdir {}'.format(directory))
		
	def bt_remote_chmod(self, sender):
		if self.connect:
			remote_file_list =  get_table_list(self.tv_remote)
			self.view_po = ui.load_view(os.path.join(pyui_path, 'popover'))
			self.view_po.name = 'Change Permission'
			self.view_po['lb_old_name'].hidden = True
			self.view_po['lb_on'].hidden = True
			self.view_po.present('popover',popover_location=(self.view.width/2,self.view.height/2))
			self.view_po['lb_nn'].text = 'Permission:'
			self.view_po['lb_old_name'].text = '\n'.join(remote_file_list)
			self.view_po['bt_cancel'].action = self.bt_cancel
			self.view_po['bt_okay'].action = self.bt_remote_chmod_okay
			self.view_po['tf_new_name'].text = '0755'
			
	def bt_remote_chmod_okay(self, sender):
		mode = self.view_po['tf_new_name'].text
		
		for remote_file in get_table_list(self.tv_remote):
			remote_dict = self.remote_dict[remote_file]
			full_path = remote_dict['full_path']
			basename = os.path.basename(full_path)

			try:
				self.ssh.command('chmod {} "{}"'.format(mode, full_path))
			except Exception as e:
				console.hide_activity()
				console.hud_alert(str(e), 'error')
				
			else:
				logging.info('color:green chmod {} to {}'.format(full_path, mode))
				
		self.view_po.close()
		self.refresh_remote_list()
		
		
		
	@ui.in_background
	def bt_connect(self, sender):
		self.host = host = self.view['tf_host'].text
		self.user = user = self.view['tf_user'].text
		self.passkey = passkey = self.view['tf_passkey'].text
		
		if host == '' or user == '' or passkey == '':
			return
		else:
			self.close_keyboard()
			
			
		port = 22
		if self.connect:
			console.show_activity('Disconnecting.....')
			if self.stash:
				#self.stash.user_action_proxy.vk_tapped( self.stash.ui.k_CD ) #kill ssh connection
				self.stash.stashssh.close = True
				
				self.stash = None
				self.busy = False
			try:
				self.ssh.close()
				
			except Exception as e:
				console.hide_activity()
				console.hud_alert(str(e), 'error')
				logging.info('color:red {}'.format(e))
				return
			console.hide_activity()
			self.connect = False
			if not sender == None:
				sender.title = 'Connect'
			self.view['bt_ssh'].enabled = False
			
		else:
			console.show_activity('Connecting.....')
			self.remote_dict = {}
			
			#self.transport = paramiko.Transport((host, port))
			#self.transport.connect(username = user, password = password)
			try:
			
				if self.pass_or_key == 'pass':
					self.ssh = SSHSession(host, username = user, password = passkey)
				elif self.pass_or_key == 'key':
					if host in self.config and 'pass_phrase' in self.config[host]:
						logging.info('color:blown Try to login by using password pharase')
						pass_phrase = self.config[host]['pass_phrase']
						self.ssh = SSHSession(host, username = user, key_file = passkey, password=pass_phrase)
					else:
						self.ssh = SSHSession(host, username = user, key_file = passkey)
						
						
			except paramiko.PasswordRequiredException as e:
				console.hide_activity()
				pass_phrase = console.password_alert('CleverSFTPClient','Private key file is encrypted\nInput password phrase','',hide_cancel_button=False)
				if not host in self.config:
					self.make_new_host(host)
				self.config[host]['pass_phrase'] = pass_phrase
				self.config.write(open(config_path, 'w'))
				self.bt_connect(sender)
				return
				
			except Exception as e:
				if e.message == 'Unable to parse key file' or e.message == 'Not a valid RSA private key file (bad ber encoding)' or e.message == 'Not a valid DSS private key file (bad ber encoding)':
					console.hud_alert('Wrong pass phrase','error')
					pass_phrase = console.password_alert('CleverSFTPClient','Private key file is encrypted\nInput pass phrase','',hide_cancel_button=False)
					if not host in self.config:
						self.make_new_host(host)
					self.config[host]['pass_phrase'] = pass_phrase
					self.config.write(open(config_path, 'w'))
					self.bt_connect(sender)
					return
					
				console.hide_activity()
				console.hud_alert(str(e), 'error')
				logging.info('color:red {}'.format(e))
				print(traceback.format_exc())
				return
				
			self.connect = True
			console.hud_alert('Successful!!',duration=0.5)
		
			self.view['bt_ssh'].enabled = True
			#threading.Thread(target=self.bt_ssh, args=(None,)).start()
			try:
				try:
					from stash.stash import StaSh
				except:
					stash_installer()
				finally:
					from stash.stash import StaSh
					
				self.stash = StaSh()
				self.stash.ui.width, self.stash.ui.height = ui.get_screen_size()
				self.stash.csc_ssh = self.ssh.ssh
				self.stash("'{}'&".format(os.path.join(core_path, 'ssh')))
				
				
			except Exception as e:
				print('fr'+str(e))
				
			#self.csc_ssh = threading.enumerate()[0].csc_ssh
			
			
			if not host in self.config:
				self.make_new_host(host)
			self.config[host]['user'] = user
			if self.pass_or_key == 'pass':
				self.config[host]['password'] = passkey
			elif self.pass_or_key == 'key':
				self.config[host]['key'] = passkey
				
			self.config.write(open(config_path, 'w'))
			
			#self.sftp = paramiko.SFTPClient.from_transport(self.transport)
			self.sftp = self.ssh.sftp
			self.sftp.chdir('.')
			self.remotePath = self.sftp.getcwd()
			
			self.refresh_remote_list()
			
			sender.title = 'Disconnect'
			console.hide_activity()
			
			logging.info( 'color:blown Connect with {}:{}'.format(host,port))
			logging.info( 'color:blown Name {}'.format(self.config[host]['name']))
			
			
	def bt_upload(self, sender):  #local
		@ui.in_background
		def upload():
			for local_file in get_table_list(self.tv_local):
				local_dict = self.local_dict[local_file]
				full_path = local_dict['full_path']
				basename = local_file
				type = local_dict['type']
				if type == 'dir':
					self.ssh.put_all(full_path, self.remotePath, self.progress)
				else:
					sftp_callback = self.progress(basename, os.path.join(self.remotePath, basename),'put',open_path=full_path)
					self.sftp.put(full_path.strip(), basename, sftp_callback)
			self.refresh_local_list()
		if self.connect:
			upload()
			
		self.progress_view.present('sheet')
		
		
	def bt_download(self, sender):        #remote
		@ui.in_background
		def download():
			for remote_file in get_table_list(self.tv_remote):
				remote_dict = self.remote_dict[remote_file]
				full_path = remote_dict['full_path']
				basename = remote_file
				type = remote_dict['type']
				if type == 'dir':
					try:
						self.ssh.get_all(full_path, self.local_dirname, self.progress)
					except Exception as e:
						console.hud_alert(str(e)+' and retrying', 'error')
						logging.info('color:red {} and retrying.....'.format(e))
						self.ssh.get_all(full_path.strip(), self.local_dirname, self.progress)
						
				elif type == 'file':
					to_path = os.path.join(self.local_dirname, basename)
					
					sftp_callback = self.progress(full_path, basename, 'get',open_path=to_path)
					
					try:
						self.sftp.get(basename, to_path, sftp_callback)
					except Exception as e:
						console.hud_alert(str(e)+' and retrying', 'error')
						logging.info('color:red {} and retrying.....'.format(e))
						self.sftp.get(basename.strip(), to_path, sftp_callback)
			self.refresh_remote_list()
	
		if self.connect:
			download()
			
		self.progress_view.present('sheet')
		#self.progress_view.hidden = False
		
	def check_enabled_btn(self):
		local = get_table_list(self.tv_local)
		remote = get_table_list(self.tv_remote)
		if '/..' in local:
			local_len = len(local) - 1
		else:
			local_len = len(local)
			
		if '/..' in remote:
			remote_len = len(remote) - 1
		else:
			remote_len = len(remote)
			
		if local_len == 0 or not self.tv_local.editing:
			self.view['bt_local_delete'].enabled = False
			self.view['bt_upload'].enabled = False
			self.view['bt_local_rename'].enabled = False
		else:
		
			self.view['bt_local_delete'].enabled = True
			self.view['bt_upload'].enabled = True
			self.view['bt_local_rename'].enabled = False
			
		if local_len == 1:
			self.view['bt_local_rename'].enabled = True
			
		if remote_len == 0 or not self.tv_remote.editing:
			self.view['bt_remote_delete'].enabled = False
			self.view['bt_download'].enabled = False
			self.view['bt_remote_rename'].enabled = False
			self.view['bt_remote_chmod'].enabled = False
		else:
			self.view['bt_remote_delete'].enabled = True
			self.view['bt_download'].enabled = True
			self.view['bt_remote_rename'].enabled = False
			self.view['bt_remote_chmod'].enabled = True
			
			if remote_len == 1:
				self.view['bt_remote_rename'].enabled = True
				
				
	def table_local_tapped(self, sender):
		self.check_enabled_btn()
		if not self.tv_local.editing:
			rowtext = sender.items[sender.selected_row]
			filename_tapped = rowtext
			local_dict = self.local_dict[filename_tapped]
			full_path = local_dict['full_path']
			type = local_dict['type']
			if type == 'dir':
				try:
					os.listdir(full_path)
				except Exception as e:
					console.hud_alert(str(e), 'error')
					logging.info('color:red {}'.format(e))
					return
				self.local_dirname = full_path
				self.refresh_local_list()
				
			elif type == 'file':
				threading.Thread(target=console.quicklook, args=(full_path,)).start()
				
				
	@ui.in_background
	def table_remote_tapped(self, sender):
		self.check_enabled_btn()
		if not self.tv_remote.editing:
			rowtext = sender.items[sender.selected_row]
			filename_tapped = rowtext
			remote_dict = self.remote_dict[filename_tapped]
			full_path = remote_dict['full_path']
			type = remote_dict['type']
			if type == 'dir':
				try:
					self.sftp.listdir_attr(full_path)
				except IOError as e:
					console.hud_alert(str(e), 'error')
					logging.info('color:red {}'.format(e))
					return
				self.remotePath = full_path
				
				self.refresh_remote_list()
			elif type == 'link':
				try:
					link_to = self.sftp.normalize(filename_tapped)
				except Exception as e:
					console.hud_alert('Invalid link?', 'error')
					logging.info('color:red {}'.format(e))
					return
				info = self.sftp.stat(link_to)
				if str(info)[0] == 'd':
					self.remotePath = link_to
					self.refresh_remote_list()			
					self.view['lb_remote'].text = self.remotePath
				elif str(info)[0] == '-':
					console.hud_alert('Target is file.Path is {}'.format(link_to))
					self.remotePath = os.path.dirname(link_to)
					self.refresh_remote_list()			
					self.view['lb_remote'].text = self.remotePath
					index = self.remote_list.index(os.path.basename(link_to))
					self.tableview_did_select(self.tv_remote, 0, index)
				return
				
			elif type == 'file':
				result = console.alert("CleverSFTPClient","{}".format(filename_tapped),"Edit with Pythonista editor","Download and open", 'Execute')
				if result == 1:
					to_path = os.path.join(temp_path, 'CleverSFTPClient_'+filename_tapped)
					sftp_callback = self.progress(filename_tapped, filename_tapped, 'get')
					self.sftp.get(filename_tapped.strip(), to_path, sftp_callback)
					
					self.view.close()
					editor.open_file(to_path,True)
					console.hud_alert("When finish editing file, close current tab",'',5)
					
					wait_tab_closed(os.path.basename(to_path))
					if console.alert("CleverSFTPClient","Save {}?".format(filename_tapped),'NOT Save', "Save", hide_cancel_button=True) == 2:
					
						self.view.present(hide_title_bar=True, orientations=['landscape'])
						
						sftp_callback = self.progress(filename_tapped, filename_tapped, 'put')
						
						
						self.progress_view.present('sheet')
						
						self.sftp.put(to_path, filename_tapped, sftp_callback)
					else:
						self.view.present(hide_title_bar=True, orientations=['landscape'])
					#self.progress_view.hidden = False
					
				elif result == 2:
					to_path = os.path.join(download_path, filename_tapped)
					
					self.progress_view.present('sheet')
					#self.progress_view.hidden = False
					sftp_callback = self.progress(filename_tapped, filename_tapped, 'get',open_path=to_path)
					try:
						self.sftp.get(filename_tapped, to_path, sftp_callback)
					except Exception as e:
						console.hud_alert(str(e)+' and retrying', 'error')
						logging.info('color:red {} and retrying.....'.format(e))
						sftp_callback = self.progress(filename_tapped, filename_tapped, 'get',open_path=os.path.join(download_path, filename_tapped.strip()))
						self.sftp.get(filename_tapped.strip(), to_path, sftp_callback)
						
						
					
					#self.progress_view.close()
					console.quicklook(to_path)
					
				elif result == 3:
					cmd = console.input_alert('CleverSFTPClient','Run command','"{}"'.format(self.remote_dict[filename_tapped]['full_path']), 'Execute', hide_cancel_button=False)
					self.stash.csc_send('{}\n'.format(cmd))
					self.stash.ui.present()
					self.stash.terminal.begin_editing()
					
					
					
					
	def progress(self, from_path, to_path, mode, open_path=None):
		def sftp_callback(dl, total_length):
			if total_length == 0:
				percent = 100
			else:
				percent = round((float(dl)/total_length)*100, 1)
				
			width = 534 if ui.get_screen_size()[0]+ui.get_screen_size()[1] > 1500 else ui.get_screen_size()[0]
			cell.content_view["label"].width = width*percent/100
			if cell.first:
				'''start function'''
				self.busy = True
				if cell.mode == 'get':
					logging.info('color:purple get({}, {})'.format(from_path, to_path))
				elif cell.mode == 'put':
					logging.info('color:blue put({}, {})'.format(from_path, to_path))
					
				cell.first = False
			if percent == 100 and not cell.finish:
				'''finish function'''
				self.busy = False
				cell.content_view["label"].width = width
				cell.finish = True
				if cell.mode == 'get':
					self.refresh_local_list()
				elif cell.mode == 'put':
					self.refresh_remote_list()

			cell._dl = dl - cell.pre_dl
			cell.dl_size_per_sec += cell._dl
			if time.time() - cell.dl_time >= 1:
				#to get dl speed
				cell.dl_time = time.time()
				cell.dl_speed = human_size(cell.dl_size_per_sec)
				cell.eta = (total_length - dl)/cell.dl_size_per_sec
				cell.dl_size_per_sec = 0
				cell.one_sec_passed = True
				
			eta_min = int(cell.eta/60) if int(cell.eta/60)>=10 else "0"+str(int(cell.eta/60))
			eta_sec = int(cell.eta%60) if int(cell.eta%60)>=10 else "0"+str(int(cell.eta%60))
			if eta_min == "00" and eta_sec == "00":
				eta_text = "∞"
			else:
				eta_text = "{}:{}".format(eta_min,eta_sec)
			if percent == 100:
				eta_text = "00:00"

			cell.detail_text_label.text = "{}/{} {}％ {}/s {} ".format(human_size(dl, True), human_size(total_length), percent, cell.dl_speed if cell.one_sec_passed else human_size(cell.dl_size_per_sec), eta_text)
			cell.pre_dl = dl
			
		self.progress_list.append(from_path)
		row = len(self.progress_list)-1
		
		try:
			cell = self.progress_cell_dict[row]
			
		except:
			cell = ui.TableViewCell('subtitle')
			self.progress_cell_dict[row] = cell
			
			cell_label = ui.Label(frame=(0,0,ui.get_screen_size()[0],44),name="label")
			
			cell_label.alpha = 0.5
			if mode == 'get':
				cell_label.background_color = 'purple'
				cell.text_label.text = 'Downloading {}'.format(os.path.basename(from_path))
			elif mode == 'put':
				cell_label.background_color = 'blue'
				cell.text_label.text = 'Uploading {}'.format(os.path.basename(from_path))
			cell_label.flex = "WLRTB"
			cell_label.frame = (0,0,ui.get_screen_size()[0] ,44)
			cell_label.width = 0
			cell.content_view.add_subview(cell_label)
			
			
		cell.text_label.font = ('<system-bold>', 10)
		#cell.text_label.text = '{}'.format(from_path)
		table = self.tv_progress
		table.data_source.items = self.progress_list
		
		table.reload()
		
		cell.dl_time = time.time()
		cell.dl_speed = 0
		cell.dl_size_per_sec = 0
		cell.one_sec_passed = False
		cell.eta = 0
		cell._dl = 0
		cell.pre_dl = 0
		cell.first = True
		cell.mode = mode
		cell.finish = False
		cell.open_path = open_path
		
		return sftp_callback
		
		
	def progress_tableview_cell_for_row(self, tableview, section, row):
		lst = tableview.data_source
		#_text = lst.items[row]
		try:
			cell = self.progress_cell_dict[row]
			
		except:
			cell = ui.TableViewCell('subtitle')
			
		return cell
	
	def progress_tableview_did_select(self, tableview, section, row):
		lst = tableview.data_source
		text = lst.items[row]
		cell = self.progress_cell_dict[row]
		open_path = cell.open_path
		lst.selected_row = row
		if lst.action:
			lst.action(lst)
		if open_path == None:
			console.hud_alert('Temp File', 'error')
		elif os.path.exists(open_path):
			threading.Thread(target=console.quicklook, args=(open_path,)).start()
		else:
			console.hud_alert('File not found!!', 'error')
		
		
	def refresh_table(self, table):
		#self.tv_local_selectable = False
		if table.name == 'tv_local':
			lst = ui.ListDataSource(self.local_list)
			lst.action = self.table_local_tapped
			lst.tableview_accessory_button_tapped = self.table_local_accessory_tapped
			lst.tableview_delete = self.table_local_delete
		elif table.name == 'tv_remote':
			lst = ui.ListDataSource(self.remote_list)
			lst.action = self.table_remote_tapped
			lst.tableview_accessory_button_tapped = self.table_remote_accessory_tapped
			lst.tableview_delete = self.table_remote_delete
			self.sftp.chdir(self.remotePath)
			
		table.row_height=40
		lst.tableview_can_delete = self.tableview_can_delete
		lst.tableview_cell_for_row = self.tableview_cell_for_row
		lst.tableview_did_deselect = self.tableview_did_deselect
		lst.tableview_did_select = self.tableview_did_select
		table.data_source = lst
		table.delegate = lst
		
		table.editing = False
		table.allows_multiple_selection_during_editing = True
		lst.selected_row = -1
		lst.font = ('Courier',16)
		
		lst.delete_enabled = True
		table.reload_data()
		self.check_enabled_btn()
		return
		
	def tableview_did_deselect(self, tableview, section, row):
		self.check_enabled_btn()
	
	def tableview_did_select(self, tableview, section, row):
		if tableview.name == 'tv_remote' and self.busy:
			self.tv_remote.editing = False
			console.hud_alert('Busy', 'error')
			return
			
		self.check_enabled_btn()
		lst = tableview.data_source
		text = lst.items[row]
		lst.selected_row = row
		if lst.action:
			lst.action(lst)
		
	def tableview_can_delete(self, tableview, section, row):
		lst = tableview.data_source
		if row in lst.items:
			_text = lst.items[row]
			if _text == '/..':
				return False
			else:
				return True
		else:
			return True
			
	def tableview_cell_for_row(self, tableview, section, row):
		lst = tableview.data_source
		cell = ui.TableViewCell('subtitle')
		cell.detail_text_label.text_color = '#757575'
		_text = lst.items[row]
		type = 'Unknown'
		text = ''
		
		if tableview.name == 'tv_remote' and _text in self.remote_dict:			
			remote_dict = self.remote_dict[_text]
			type = remote_dict['type']
			if not _text == '..':
				longname = remote_dict['longname'].split()
				permission = longname[0]
				user1 = longname[2]
				user2 = longname[3]
				atime = remote_dict['atime']
				mtime = remote_dict['mtime']
				if type == 'file':
					size = remote_dict['size']
					cell.detail_text_label.text = '{mtime} {permission} {user1}  {user2} {size}'.format(permission=permission, user1=user1, user2=user2, size=human_size(size), mtime=mtime)
				else:
					cell.detail_text_label.text = '{mtime} {permission} {user1} {user2}'.format(permission=permission, user1=user1, user2=user2, mtime=mtime)
							
		elif tableview.name == 'tv_local' and _text in self.local_dict:
			local_dict = self.local_dict[_text]
			type = local_dict['type']
			if not _text == '..':
				atime = local_dict['atime']
				mtime = local_dict['mtime']
	
				if type == 'file':
					size = local_dict['size']
					cell.detail_text_label.text = '{mtime} {size}'.format(size=human_size(size), mtime=mtime)
				elif type == 'dir':
					cell.detail_text_label.text = '{mtime}'.format(mtime=mtime)
				
		if type == 'dir':
			text = '🗂'+_text
		elif type == 'file':
			text = '📄'+_text
		elif type == 'link':
			text = '🔗'+_text
	
		cell.text_label.text = text
			
		if _text == '..':
			if tableview.editing:
				cell.selectable = False
		else:
			cell.accessory_type = 'detail_button'
			
		return cell
		
	def table_local_delete(self, tableview, section, row):
		lst = tableview.data_source
		_path = lst.items[row]
		path = self.local_dict[_path]['full_path']
		if console.alert("CleverSFTPClient","Detele {}?".format(_path),"No","Yes",hide_cancel_button=True) == 2:
			logging.info('color:red remove({})'.format(path))
			
			self.bt_local_delete_okay(None, [_path])
				
			del lst.items[row]
			
	def table_remote_delete(self, tableview, section, row):
		lst = tableview.data_source
		_path = lst.items[row]
		#path = self.remote_dict[_path]
		if console.alert("CleverSFTPClient","Detele {}?".format(_path),"No","Yes",hide_cancel_button=True) == 2:
			logging.info('color:red remove({})'.format(_path))
			self.bt_remote_delete_okay(None, [_path])
			del lst.items[row]
			
			
	def table_local_accessory_tapped(self, tableview, section, row):
		lst = tableview.data_source
		_path = lst.items[row]
		path = self.local_dict[_path]['full_path']
		size = os.path.getsize(path)
		console.alert('Name : {}\nSize : {}'.format(_path, human_size(size)), hide_cancel_button=True)
		
		
	def table_remote_accessory_tapped(self, tableview, section, row):
		lst = tableview.data_source
		_path = lst.items[row]
		remote_dict = self.remote_dict[_path]
		path = remote_dict['full_path']
		file_type = remote_dict['type']
		if file_type == 'dir':
			if console.alert('CleverSFTPClient', 'Name : {}'.format(path), 'Cd this dir', hide_cancel_button=False) == 1:
				self.stash.csc_send('cd "{}"\n'.format(path))
				self.stash.ui.present()
				self.stash.terminal.begin_editing()
		
		
	def refresh_local_list(self):
		self.local_dict = {}
		files = []
		
		if self.local_dirname == '/':
			dirs = []
		else:
			dirs  = ['..']
			full_path = '/'.join(self.local_dirname.split('/')[:-1])
			if full_path == '':
				full_path = '/'
			self.local_dict['..'] = {'full_path':full_path, 'type':'dir'}
			
		for entry in sorted(os.listdir(self.local_dirname)):
			full_path = os.path.join(self.local_dirname, entry)
			if os.path.exists(full_path): #リンク先のないリンクファイルを除く
				info = os.stat(full_path)
				size = info.st_size
				mtime = info.st_mtime #最終変更時刻
				atime = info.st_atime #最終アクセス時刻
				mtime = datetime.fromtimestamp(mtime)
				atime = datetime.fromtimestamp(atime)
				if os.path.isdir(full_path):
					dirs.append(entry)
					local_dict = {'full_path':full_path, 'type':'dir', 'atime':atime, 'mtime':mtime}
				else:
					
					files.append(entry)
					local_dict = {'full_path':full_path, 'size':size, 'type':'file', 'atime':atime, 'mtime':mtime}
				self.local_dict[entry] = local_dict
			
		dirs.extend(files)
		all = dirs
		self.local_list = all
		
		if to_abs_path() in self.local_dirname:
			if self.local_dirname == to_abs_path():
				self.view['lb_local'].text = 'Documents'
			else:
				self.view['lb_local'].text = 'Documents/'+to_relpath(self.local_dirname)
		else:
			self.view['lb_local'].text = self.local_dirname
			
		self.refresh_table(self.tv_local)
		
			
	def refresh_remote_list(self):
		
		try:
			attr = self.sftp.listdir_attr(self.remotePath)
		except Exception as e:
			console.hide_activity()
			console.hud_alert(str(e), 'error')
			return 
			
		self.remote_dict = {}
		files = []
		
		if self.remotePath == '/':
			dirs  = []
		else:
			dirs  = ['..']
			full_path = '/'.join(self.remotePath.split('/')[:-1])
			if full_path == '':
				full_path = '/'
			self.remote_dict['..'] = {'full_path':full_path, 'type':'dir'}

		
		for entry in attr:
			size = entry.st_size
			longname = entry.longname
			mtime = entry.st_mtime #最終変更時刻
			atime = entry.st_atime #最終アクセス時刻
			mtime = datetime.fromtimestamp(mtime)
			atime = datetime.fromtimestamp(atime)
			longname = longname
			type = 'Unknown'
			path = str(entry)[55:]
			full_path = os.path.join(self.remotePath, path)
			
			if str(entry)[0] ==  'd':	
				type = 'dir'
				dirs.append(path)
			elif str(entry)[0] ==  '-':
				type = 'file'
				files.append(path)
			elif str(entry)[0] ==  'l':
				type = 'link'
				files.append(path)
				
			remote_dict = {'full_path':full_path, 'size':size, 'longname':longname, 'type':type, 'atime':atime, 'mtime':mtime}
			self.remote_dict[path] = remote_dict
			
		all = sorted(dirs)
		for file in sorted(files):
			all.append(file)
		self.remote_list = all
		self.view['lb_remote'].text = self.remotePath
		self.refresh_table(self.tv_remote)
		
	@ui.in_background
	def bg_hud_alert(self, text, icon='success', duration=1.8):
		console.hud_alert(text, icon, duration)
		
def to_abs_path(*value):
	import os
	abs_path = os.path.join(os.path.expanduser('~'),'Documents')
	for _value in value:
		abs_path = os.path.join(abs_path,_value)
	return abs_path
	
app_root_path = os.path.dirname(__file__)
core_path = os.path.join(app_root_path, 'core')
pyui_path = os.path.join(core_path, 'pyui')
temp_path = os.path.join(app_root_path, 'temp')
download_path = os.path.join(app_root_path, 'download')
config_path = os.path.join(app_root_path, 'config.ini')

CleverSFTPClient()

