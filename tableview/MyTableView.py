# coding: utf-8

# https://gist.github.com/beer2011/f077d2f6401fe9b4c1d3

import ui
import console

class MyTableView(object):
	def __init__(self):
		self.list = [{'title': 'Vegitable'},
		{'title': 'Fruits'},
		{'title': 'Fish'}]
		
		self.tv = ui.TableView()
		self.tv.name = 'Kind'
		self.tv.delegate = self
		self.tv.data_source = self
		
		nv = ui.NavigationView(self.tv)
		nv.name = 'Foods'
		nv.present('sheet')
		
	def tableview_did_select(self, tableview, section, row):
		tv = ui.TableView()
		tv.name = self.list[row]['title']
		
		if tv.name == 'Fruits':
			sub_ds = SubTableView()
			tv.data_source = sub_ds
			tv.delegate  = sub_ds
			tableview.navigation_view.push_view(tv)
		else:
			tv.delegate  = self
			tableview.navigation_view.push_view(tv)
			
	def tableview_number_of_sections(self, tableview):
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.list)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.list[row]['title']
		return cell
		
class SubTableView(object):
	def __init__(self):
		self.fruits = [{'title': 'Banana'},
		{'title': 'Orenge'},
		{'title': 'Grape'}]
		
		self.tv = ui.TableView()
		self.tv.delegate = self
		self.tv.data_source = self
		
	def tableview_did_select(self, tableview, section, row):
		tv = ui.TableView()
		tv.name = self.fruits[row]['title']
		tv.delegate  = self
		tableview.navigation_view.push_view(tv)
		
	def tableview_number_of_sections(self, tableview):
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.fruits)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.fruits[row]['title']
		return cell
		
		
### main ########################
MyTableView()

