# coding: utf-8

# https://forum.omz-software.com/topic/3104/refreshing-replacing-tableview-data/5

import ui
import dialogs

class tv (object):
	def __init__(self):
		self.data = []
		
	def tableview_did_select(self, tableview, section, row):
		pass
		
	def tableview_number_of_sections(self, tableview):
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.data[row]
		return cell
		
data = tv()
v = ui.TableView()
def add(sender):
	data.data.append(dialogs.input_alert(title='Please Enter'))
	v.reload_data()
if __name__ == '__main__':

	v.right_button_items = [ui.ButtonItem(title='Add',action=add)]
	v.data_source = data
	v.delegate = data
	v.present()

