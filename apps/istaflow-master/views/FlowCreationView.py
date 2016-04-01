# coding: utf-8
import ui
import console

dbo = None
class FlowCreationView(object):
	def __init__(self, elements, saveCallBack):
		self.elements = elements
		self.saveCallBack = saveCallBack
		self.extraRows = 1
		self.title = ''

	def tableview_did_select(self, tableview, section, row):
		pass
		
	def tableview_title_for_header(self, tableview, section):
		pass

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.elements)+self.extraRows
		
	def tableview_cell_for_row(self, tableview, section, row):
		if row > 0:
			cell = ui.TableViewCell('subtitle')
			cell.selectable = False
			cell.text_label.text = self.elements[row-self.extraRows].get_title()
			cell.detail_text_label.text = self.elements[row-self.extraRows].get_description()
			cell.image_view.image = ui.Image.named(self.elements[row-self.extraRows].get_icon())
			cell.selectable = True
			return cell
		else:
			cell = ui.TableViewCell()
			cell.selectable = False
			if tableview.editing:
				title = 'Done'
			else:
				title = 'Edit'
			editButton = ui.Button(title=title)
			editButton.width *= 1.4
			editButton.action = swap_edit
			editButton.y = cell.height/2 - editButton.height/2
			editButton.x = cell.width/2+editButton.width/2
			cell.add_subview(editButton)
			titleButton = ui.Button(title='Change Title')
			titleButton.y = cell.height/2 - editButton.height/2
			titleButton.x = titleButton.width/2
			titleButton.action = self.change_title
			cell.add_subview(titleButton)
			return cell
	
	@ui.in_background		
	def change_title(self, sender):
		self.title = console.input_alert('Please enter a title','',self.title,'Ok',False)
		table_view.name = self.title
		
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		if row >= self.extraRows:
			return True
		else:
			return False

	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		if row >= self.extraRows:
			return True
		else:
			return False

	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		self.elements.pop(row-self.extraRows)
		del_row([row])

	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		self.elements.insert(to_row-self.extraRows, self.elements.pop(from_row-self.extraRows))


table_view = ui.TableView()
def get_view(elements, cb):
	dbo = FlowCreationView(elements = elements, saveCallBack = cb)
	table_view.name = 'Flow'
	table_view.data_source = dbo
	table_view.delegate = dbo
	return table_view

def swap_edit(sender):
	if table_view.editing:
		table_view.editing = False
		sender.title = 'Edit'
	else:
		table_view.editing = True
		sender.title = 'Done'

def del_row(row):
	table_view.delete_rows(row)