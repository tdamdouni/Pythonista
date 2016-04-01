# coding: utf-8
import sys
if '..' not in  sys.path:
	sys.path.insert(0, '..')
import ui
from Utilities import sqlite3utils
import tableobjectview

class dbobjectsview(object):
	def __init__(self, dbp, navview):
		self.dbpath = dbp
		self.naview = navview
		s3u = sqlite3utils.sqlite3utils(dbpath=dbp)
		self.tables = s3u.get_all_tables_name()
		self.views = s3u.get_all_views_name()
		self.systemtables = s3u.get_all_system_tables()
		s3u.close_db()

	def tableview_did_select(self, tableview, section, row):
		t = tableobjectview.tbo()
		s3u = sqlite3utils.sqlite3utils(dbpath=self.dbpath)
		if section == 0:
			self.naview.navigation_view.push_view(t.get_view(self.dbpath, self.tables[row]))
		elif section == 1:
			self.naview.navigation_view.push_view(t.get_view(self.dbpath, self.views[row]))
		elif section == 2:
			self.naview.navigation_view.push_view(t.get_view(self.dbpath, self.systemtables[row]))
		s3u.close_db()
		
	def tableview_title_for_header(self, tableview, section):
		if section == 0 and len(self.tables) > 0:
			return 'Tables'
		elif section == 1 and len(self.views) > 0:
			return 'Views'
		elif section == 2 and len(self.systemtables) > 0:
			return 'System Tables'

	def tableview_number_of_sections(self, tableview):
		return 3

	def tableview_number_of_rows(self, tableview, section):
		if section == 0:
			return len(self.tables)
		elif section == 1:
			return len(self.views)
		else:
			return len(self.systemtables)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		if section == 0:
			cell.text_label.text = self.tables[row]
		elif section == 1:
			cell.text_label.text = self.views[row]
		else:
			cell.text_label.text = self.systemtables[row]
		
		cell.selectable = True
		return cell

def get_view(dbpath, navview):
	dbo = dbobjectsview(dbpath, navview)
	table_view = ui.TableView()
	table_view.name = dbpath
	table_view.data_source = dbo
	table_view.delegate = dbo
	return table_view