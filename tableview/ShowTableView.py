# coding: utf-8

# https://github.com/humberry/ui-tutorial/blob/master/ShowTableView.py

import console, os, ui

class ShowTableView(object):
	def __init__(self):
		self.view = ui.load_view('ShowTableView')
		self.view.present('fullscreen')
		self.view.name = 'ShowTableView'
		self.bt_empty_action(None)
		
	def bt_dir_action(self, sender):
		dir_items = os.listdir(os.getcwd())
		tv1 = self.view['tableview1']
		tv1.data_source = tv1.delegate = ui.ListDataSource(dir_items)
		tv1.data_source.delete_enabled = tv1.editing = False
		tv1.reload_data()
		
	def bt_empty_action(self, sender):
		lst = ui.ListDataSource([])
		tv1 = self.view['tableview1']
		tv1.data_source = tv1.delegate = ui.ListDataSource([])
		tv1.data_source.delete_enabled = tv1.editing = False
		tv1.reload_data()
		
	def bt_picture_action(self, sender):
		lst = ui.ListDataSource([{'title':'none','accessory_type':'none'},
		{'title':'checkmark','accessory_type':'checkmark'},
		{'title':'detail_button','accessory_type':'detail_button'},
		{'title':'detail_disclosure_button','accessory_type':'detail_disclosure_button'},
		{'title':'disclosure_indicator','accessory_type':'disclosure_indicator'},
		{'title':'image24 and checkmark','image':'ionicons-images-24','accessory_type':'checkmark'},
		{'title':'image32','image':'ionicons-alert-32'},
		{'title':'image256','image':'ionicons-alert-circled-256'},
		{'title':'frog','image':'Frog_Face'},
		{'title':'OwnImage','image':'Image/OwnImage.png'}])
		tv1 = self.view['tableview1']
		tv1.data_source = tv1.delegate = lst
		tv1.data_source.delete_enabled = tv1.editing = False
		lst.action = self.tv1_action
		tv1.reload_data()
		
	@ui.in_background
	def tv1_action(self, sender):
		info = sender.items[sender.selected_row]
		console.alert('info', '\n'.join(['{} = {}'.format(i, info[i]) for i in info]))
		
ShowTableView()

