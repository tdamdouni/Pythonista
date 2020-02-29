# coding: utf-8

# https://gist.github.com/henryiii/5f38c0668b73c2e87ff0

from __future__ import print_function
import ui
import os
import console

class MyTableViewDataSource (object):
	sel = [None]
	
	def __init__(self, base_dir = '.'):
		self.dir = base_dir
		_, folders, files = next(os.walk(base_dir))
		self.data = (folders,files)
	
	def tableview_number_of_sections(self, tableview):
		return 2

	def tableview_number_of_rows(self, tableview, section):
		return len(self.data[section])

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.accessory_type = ('disclosure_indicator', 'detail_button')[section]
		cell.text_label.text = self.data[section][row]
		return cell

	def tableview_title_for_header(self, tableview, section):
		return ('Folders','Files')[section]

	def tableview_did_select(self, tableview, section, row):
		'@type tableview: ui.TableView'
		if section == 0:
			dir = os.path.join(self.dir, self.data[section][row])
			newv = FileViewer(dir)
			nav = tableview.superview.navigation_view
			nav.push_view(newv.view)
		else:
			self.sel[0] = os.path.join(self.dir, self.data[section][row])
			tableview.superview.navigation_view.close()

	def tableview_accessory_button_tapped(self, tableview, section, row):
		full = os.path.join(self.dir,self.data[section][row])
		stats =  os.stat(full)
		console.hud_alert('Size: {0} KB'.format(stats.st_size//1024))
		

class FileViewer(object):
	def __init__(self, base_dir = '.', *args, **kargs):
		self.table = ui.TableView(*args, **kargs)
		self.table.name = 'FileTable'
		self.src = MyTableViewDataSource(base_dir)
		self.table.data_source = self.src
		self.table.delegate = self.src
		self.table.flex = 'WHTBLR'

		self.view = ui.View(name = base_dir)
		self.view.background_color = 'white'
		self.view.add_subview(self.table)
		
	@property
	def selection(self):
		return self.src.sel[0]

fv = FileViewer()
nv = ui.NavigationView(fv.view)
nv.name = 'File Selector' 
nv.present('sheet')
#nv.wait_modal()
print(fv.selection)