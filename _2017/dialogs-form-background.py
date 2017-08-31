# https://forum.omz-software.com/topic/4298/change-background-color-in-the-dialogs-form

import ui
import dialogs

def my_tableview_cell_for_row(self, tv, section, row):
	if self.view.background_color != 'blue':
		self.view.background_color = 'blue'
	return self.cells[section][row]
	
dialogs._FormDialogController.tableview_cell_for_row = my_tableview_cell_for_row

fields = [{'title':'title1','type':'text','value':''}, {'title':'title2','type':'text','value':''}]
f = dialogs.form_dialog(title='dialog title', done_button_title='ok',fields=fields, sections=None)

