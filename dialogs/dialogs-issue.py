# coding: utf-8

# https://forum.omz-software.com/topic/2601/dialogs-issue

import ui
import dialogs

def dia_test(sender):
	dialogs.form_dialog(title='Test',fields=[{'type':'text','title':'Some Title'}])
	
class testtv (object):

	def tableview_did_select(self, tableview, section, row):
		dia_test(None)
		
	def tableview_number_of_rows(self, tv, s):
		return 1
		
	def tableview_cell_for_row(self, tv, s, r):
		cell = ui.TableViewCell('default')
		cell.text_label.text = 'Test'
		cell.selectable = True
		return cell
		
view = ui.TableView()
dbo = testtv()
view.data_source = dbo
view.delegate = dbo
view.right_button_items = [ui.ButtonItem(title='Press me!', action=dia_test)]
view.present()

#==============================

import ui
import dialogs

@ui.in_background
def dia_test(sender):
	dialogs.form_dialog(title='Test',fields=[{'type':'text','title':'Some Title'}])
	
class testtv (object):

	def tableview_did_select(self, tableview, section, row):
		dia_test(None)
		
	def tableview_number_of_rows(self, tv, s):
		return 1
		
	def tableview_cell_for_row(self, tv, s, r):
		cell = ui.TableViewCell('default')
		cell.text_label.text = 'Test'
		cell.selectable = True
		return cell
		
view = ui.TableView()
dbo = testtv()
view.data_source = dbo
view.delegate = dbo
view.right_button_items = [ui.ButtonItem(title='Press me!', action=dia_test)]
view.present()

