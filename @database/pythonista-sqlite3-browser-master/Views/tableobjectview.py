# coding: utf-8
import sys
if '..' not in  sys.path:
	sys.path.insert(0, '..')
import ui
from Utilities import sqlite3utils

class tableobjectsview(object):
	def __init__(self, dbp, table):
		self.dbpath = dbp
		s3u = sqlite3utils.sqlite3utils(dbpath=dbp)
		self.tinfo = s3u.table_info(table)
		self.iinfo = s3u.index_info(table)
		s3u.close_db()

	def tableview_did_select(self, tableview, section, row):
		return
		
	def tableview_title_for_header(self, tableview, section):
		if section == 0 and len(self.tinfo) > 0:
			return 'Columns'
		elif section == 1 and len(self.iinfo) > 0:
			return 'Indexes'

	def tableview_number_of_sections(self, tableview):
		return 2

	def tableview_number_of_rows(self, tableview, section):
		if section == 0:
			return len(self.tinfo)
		elif section == 1:
			return len(self.iinfo)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		if section == 0:
			nullable = 'False'
			if self.tinfo[row][3] == 1:
				nullable = 'True'
			cell.text_label.text = self.tinfo[row][1]
			cell.detail_text_label.text = 'Type: ' + self.tinfo[row][2] + ' Nullable: ' + nullable + ' Default: ' + str(self.tinfo[row][4])
		elif section == 1:
			cell.text_label.text = self.iinfo[row][1]
		cell.selectable = False
		return cell
		
class dataobjectview(object):
	def __init__(self, dbp, table):
		self.currentid = 1
		self.dbpath = dbp
		s3u = sqlite3utils.sqlite3utils(dbpath=dbp)
		self.tkeys, self.tdata = s3u.get_table_data(table)
		self.maxnumber = len(self.tdata)
		s3u.close_db()

	def tableview_did_select(self, tableview, section, row):
		return
		
	def tableview_title_for_header(self, tableview, section):
		return

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		if section == 0:
			return len(self.tdata[self.currentid-1])+1
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('value1')
		if section == 0:
			if row == 0:
				cell.text_label.text = 'Record'
				cell.detail_text_label.text = self.return_count_label()
			else:
				cell.text_label.text = str(self.tkeys[row-1])
				cell.detail_text_label.text = str(self.tdata[self.currentid-1][row-1])
		cell.selectable = False
		return cell
		
	def initial_button_config(self):
		if self.currentid >= self.maxnumber:
			return False, False
		else:
			return True, False
			
	def prev(self):
		self.currentid -=1
		if self.currentid > 1:
			return True, True
		else:
			return True, False
	
	def next(self):
		self.currentid +=1
		if self.currentid >= self.maxnumber:
			return False, True
		else:
			return True, True
	
	def return_count_label(self):
		return str(self.currentid)+'/'+str(self.maxnumber)
	

class tbo (object):
	def __init__(self):
		self.schema_v = ui.TableView('grouped')
		self.data_v = ui.TableView()
		self.nbutton = ui.Button(title='Next')
		self.pbutton = ui.Button(title='Prev')
		
	def test(self, sender):
		if sender.selected_index == 0:
			self.schema_v.hidden = False
			self.data_v.hidden = True
			self.pbutton.hidden = True
			self.nbutton.hidden = True
		elif sender.selected_index == 1:
			self.schema_v.hidden = True
			self.data_v.hidden = False
			self.pbutton.hidden = False
			self.nbutton.hidden = False
	
	def next(self, sender):
		self.nbutton.enabled, self.pbutton.enabled = self.ov.next()
		self.data_v.reload_data()
		
	def prev(self, sender):
		self.nbutton.enabled, self.pbutton.enabled = self.ov.prev()
		self.data_v.reload_data()

	def get_view(self, dbpath, tablename):
		self.schema_v = ui.TableView('grouped')
		self.data_v = ui.TableView()
		schema_view = self.schema_v
		data_view = self.data_v
		dbo = tableobjectsview(dbpath, tablename)
		self.ov = dataobjectview(dbpath, tablename)
		w, h = ui.get_screen_size()
		schema_view.name = tablename
		schema_view.data_source = dbo
		schema_view.delegate = dbo
		data_view.name = tablename
		data_view.data_source = self.ov
		data_view.delegate = self.ov
		seg = ui.SegmentedControl()
		seg.segments = ['Schema','Data']
		seg.selected_index = 0
		seg.action = self.test
		seg.width = w/3
		seg.x = w/2 - (seg.width/2)
		seg.y = seg.height / 2
		self.pbutton.y = seg.y
		self.nbutton.y = seg.y
		self.pbutton.x = seg.x - (seg.width/2)
		self.nbutton.x = seg.x + seg.width
		self.pbutton.width = seg.width/2
		self.nbutton.width = seg.width/2
		self.pbutton.hidden = True
		self.nbutton.hidden = True
		self.pbutton.action = self.prev
		self.nbutton.action = self.next
		self.nbutton.enabled, self.pbutton.enabled = self.ov.initial_button_config()
		t = ui.View(frame=(0,0,w,h))
		t.background_color = (0.92,0.92,0.95)
		t.width = w
		t.height = h
		schema_view.width = w
		schema_view.height = t.height * 0.9
		schema_view.y = 2 * seg.height
		data_view.width = w
		data_view.height = t.height * 0.9
		data_view.y = 2 * seg.height
		data_view.hidden = True
		schema_view.hidden = False
		self.schema_v = schema_view
		self.data_v = data_view
		t.add_subview(self.schema_v)
		t.add_subview(self.data_v)
		t.add_subview(seg)
		t.add_subview(self.pbutton)
		t.add_subview(self.nbutton)
		return t
	