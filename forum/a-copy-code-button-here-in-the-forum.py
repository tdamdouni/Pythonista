# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2022/a-copy-code-button-here-in-the-forum/14_

# coding: utf-8

# WARNING - HANGS AFTER COPY CODE, THEN RUNNING
# AGAIN WITH THE COPIED CODE ON THE CLIPBOARD.
# HAVE TO RESTART PYTHONISTA!

import ui
import clipboard
import console

class OmzFourmCopy(ui.View):
	def __init__(self, data_list):
		self.data = data_list
		# create copy title btn
		btn = ui.ButtonItem('Copy Code')
		btn.action = self.copy_code
		self.right_button_items = [btn]
		
		
		# create the tableview, set the data_source
		# and delegate to self.
		tv = ui.TableView(name = 'tv1')
		tv.name = 'tv1'
		tv.data_source = self
		tv.border_width = .5
		tv.delegate = self
		
		
		#create textview
		txtv = ui.TextView(name = 'txtv')
		txtv.font = ('Courier', 14)
		
		
		# select the first code block
		tv.selected_row = 0
		txtv.text = self.data[0]
		
		
		self.add_subview(txtv)
		self.add_subview(tv)
		
	def copy_code(self, sender):
		if self['txtv'].text:
			code = self.data[self['tv1'].selected_row[0]]
			#clipboard.set(self['txtv'].text)
			clipboard.set(code)
			console.hud_alert('Copied', duration = .5)
			self.close()
			
	def layout(self):
		self.frame = self.bounds
		tv = self['tv1']
		
		tv.frame = (0,0,self.width * .20, self.height)
		
		self['txtv'].frame = (tv.width, 0, self.width - tv.width, self.height)
		
	def tableview_cell_for_row(self, tableview, section, row):
	
		cell = ui.TableViewCell()
		cell.text_label.text = 'Code {}'.format(row + 1)
		return cell
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.data)
		
	def tableview_did_select(self, tableview, section, row):
		self['txtv'].text = self.data[row]
		
use_appex = False
try:
	# appex is only available in 1.6 beta, fail gracefully when running in 1.5
	import appex
	use_appex = appex.is_running_extension()
except:
	pass
	
def main():
	lst = []
	if use_appex:
		url = appex.get_url()
	else:
		url = clipboard.get()
		
	if 'omz-forums' not in url or len(url.splitlines()) > 1:
		#print 'No forum URL'
		lst.append('-1')  # i know this is crappy.
		return lst
		
	import requests
	import bs4
	html = requests.get(url).text
	soup = bs4.BeautifulSoup(html)
	pre_tags = soup.find_all('pre')
	if pre_tags:
		text = ''
		#text = ('\n#%s\n\n' % ('=' * 30)).join([p.get_text() for p in pre_tags])
		
		for p in pre_tags:
			lst.append(p.get_text())
		#clipboard.set(text)
		#print 'Code copied (%i lines)' % (len(text.splitlines()))
	else:
		#print 'No code found'
		pass
		
	return lst
	
	
if __name__ == '__main__':
	lst =  main()
	if len(lst) == 0:
		console.alert('No code found')
	elif lst[0] == '-1':
		console.alert('omz-forums, not in url')
	else:
		x = OmzFourmCopy(lst)
		x.present()
		
###==============================

import ui, console

class TestTableView(ui.View):
	def __init__(self):
	
		# crap data for the tableview
		self.data = range(100)
		
		#create tableview
		tv = ui.TableView()
		tv.name = 'tv' # name param does not work
		
		# the data/delagate methods called by
		# tableview will be called in this class
		tv.data_source = self
		tv.delegate = self
		
		# add the table
		self.add_subview(tv)
		
	def layout(self):
		self['tv'].frame = self.bounds
		
	# prototype methods copied from pytonista help file
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		
		# IMPORTANT
		# ui.TableViewCell() has 4 params
		# empty = default
		# subtitle
		# value1
		# value2
		
		# beware, if you create a cell with no params
		# the default, cell.detail_text_label does
		# not exist and will produce an error if
		# you try and reference it! the other cell
		# types subtitle, value1, value2 have the
		# cell.detail_text_label.
		# you can also mix cell types, if it makes
		# sense.
		
		
		cell = ui.TableViewCell('subtitle')
		cell.text_label.text = 'row {}'.format(row)
		cell.detail_text_label.text = '{}'.format(row * 10)
		return cell
		
	def tableview_title_for_header(self, tableview, section):
		# Return a title for the given section.
		# If this is not implemented, no section headers will be shown.
		#return 'Some Section'
		pass
		
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return True
		
	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return True
		
	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		pass
		
	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		# Called when the user moves a row with the reordering control (in editing mode).
		pass
		
	# delegate method prototypes, copied from
	#pythonista help files
	def tableview_did_select(self, tableview, section, row):
		# Called when a row was selected.
		console.hud_alert('Row {} selected'.format(self.data[row]), duration = 1)
		#pass
		
	def tableview_did_deselect(self, tableview, section, row):
		# Called when a row was de-selected (in multiple selection mode).
		pass
		
	def tableview_title_for_delete_button(self, tableview, section, row):
		# Return the title for the 'swipe-to-***' button.
		return 'Delete'
		
		
if __name__ == '__main__':
	ttv = TestTableView().present()
	
###==============================

import ui, console

class TestTableView(ui.View):
	def __init__(self):
	
		# crap data for the tableview
		self.data = range(100)
		
		#create tableview
		tv = ui.TableView()
		tv.name = 'tv' # name param does not work
		
		# the data/delagate methods called by
		# tableview will be called in this class
		tv.data_source = self
		tv.delegate = self
		
		# add the table
		self.add_subview(tv)
		
	def layout(self):
		self['tv'].frame = self.bounds
		
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.text_label.text = 'row {}'.format(row)
		cell.detail_text_label.text = '{}'.format(row * 10)
		return cell
		
	def tableview_did_select(self, tableview, section, row):
		console.hud_alert('Row {} selected'.format(self.data[row]), duration = 1)
		
if __name__ == '__main__':
	ttv = TestTableView().present('sheet')

