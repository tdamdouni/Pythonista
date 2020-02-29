# coding: utf-8

# https://github.com/humberry/ui-tutorial/blob/master/Three-Column-Sortable-TableView.py

# https://forum.omz-software.com/topic/2940/share-code-tableview

from __future__ import print_function
import ui, os, datetime
from operator import itemgetter

class MyTableViewDataSource (object):
	def __init__(self, row_height):
		self.row_height = row_height
		self.width = None
		
	def tableview_number_of_rows(self, tableview, section):
		return len(tableview.data_source.items)
		
	def tableview_cell_for_row(self, tableview, section, row):
		self.width, height = ui.get_screen_size()
		cell = ui.TableViewCell()
		cell.bounds = (0,0,self.width,self.row_height)
		self.make_labels(cell, tableview.data_source.items[row][0], 0)
		self.make_labels(cell, tableview.data_source.items[row][1], 1)
		self.make_labels(cell, tableview.data_source.items[row][2], 2)
		return cell
		
	def make_labels(self, cell, text, pos):
		label = ui.Label()
		label.border_color = 'lightgrey'
		label.border_width = 0.5
		if pos == 2:
			label.text = str(datetime.datetime.fromtimestamp(text))
		else:
			label.text = str(text)
		label.frame = (pos*self.width/3,0,self.width/3,self.row_height)
		label.alignment = ui.ALIGN_CENTER
		cell.content_view.add_subview(label)
		
class MyTableViewDelegate(object):
	def tableview_did_select(self, tableview, section, row):
		print('select')
		
	def tableview_did_deselect(self, tableview, section, row):
		print('deselect')
		
class MyTableView(ui.View):
	def __init__(self):
		self.dirs = []
		self.files = []
		self.select_color = 'lightgrey'
		self.unselect_color = 'white'
		self.active_button = None
		self.button_height = 50
		self.btn_name = self.make_buttons('Name')
		self.btn_size = self.make_buttons('Size')
		self.btn_date = self.make_buttons('Date')
		self.tv = ui.TableView()
		self.tv.row_height = 30
		self.tv.data_source = MyTableViewDataSource(self.tv.row_height)
		self.get_dir()
		self.all_items = self.dirs + self.files
		self.tv.data_source.items = self.all_items
		self.name = 'TableView-Test'
		#self.tv.delegate = MyTableViewDelegate()
		self.tv.allows_selection = False
		self.add_subview(self.tv)
		self.present('full_screen')
		
	def make_buttons(self, name):
		button = ui.Button()
		button.name = name
		button.title = name
		button.border_color = 'blue'
		button.border_width = 1
		button.corner_radius = 3
		button.background_color = self.unselect_color
		button.action = self.btn_action
		self.add_subview(button)
		return button
		
	def btn_action(self, sender):
		if self.active_button == sender.name:
			if sender.background_color == (1.0, 1.0, 1.0, 1.0):    #change this if unselect_color isn't white
				sender.background_color = self.select_color
				if sender.name == self.btn_name.name:
					self.all_items = sorted(self.all_items, key=itemgetter(0))
				elif sender.name == self.btn_size.name:
					self.all_items = sorted(self.all_items, key=itemgetter(1))
				elif sender.name == self.btn_date.name:
					self.all_items = sorted(self.all_items, key=itemgetter(2))
			else:
				sender.background_color = self.unselect_color
				if sender.name == self.btn_name.name:
					self.all_items = sorted(self.all_items, key=itemgetter(0), reverse=True)
				elif sender.name == self.btn_size.name:
					self.all_items = sorted(self.all_items, key=itemgetter(1), reverse=True)
				elif sender.name == self.btn_date.name:
					self.all_items = sorted(self.all_items, key=itemgetter(2), reverse=True)
		else:
			if self.active_button == None:
				self.active_button = sender.name
			if sender.name == self.btn_name.name:
				self.btn_name.background_color = self.select_color
				self.all_items = sorted(self.all_items, key=itemgetter(0))
			else:
				self.btn_name.background_color = self.unselect_color
			if sender.name == self.btn_size.name:
				self.btn_size.background_color = self.select_color
				self.all_items = sorted(self.all_items, key=itemgetter(1))
			else:
				self.btn_size.background_color = self.unselect_color
			if sender.name == self.btn_date.name:
				self.btn_date.background_color = self.select_color
				self.all_items = sorted(self.all_items, key=itemgetter(2))
			else:
				self.btn_date.background_color = self.unselect_color
		self.tv.data_source.items = self.all_items
		self.tv.reload()
		self.active_button = sender.name
		
	def layout(self):
		self.tv.reload()
		self.btn_name.frame =(0*self.width/3, 0, self.width/3, self.button_height)
		self.btn_size.frame =(1*self.width/3, 0, self.width/3, self.button_height)
		self.btn_date.frame =(2*self.width/3, 0, self.width/3, self.button_height)
		self.tv.frame = (0, self.button_height, self.width, self.height - self.button_height)
		
	def get_dir(self):
		path = os.getcwd()
		self.dirs  = [] if path == os.path.expanduser('~') else [['..', '<DIR>', 0.0]]
		self.files = []
		for entry in sorted(os.listdir(path)):
			full_pathname = path + '/' + entry
			if os.path.isdir(full_pathname):
				date = os.path.getmtime(full_pathname)
				self.dirs.append((entry, '<DIR>', date))
			else:
				size = os.path.getsize(full_pathname)
				date = os.path.getmtime(full_pathname)
				self.files.append((entry, size, date))
				
MyTableView()

