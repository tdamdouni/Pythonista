# coding: utf-8
import ui

class ElementListView(object):
	def __init__(self, elements, selectedCallBack):
		self.elements = elements
		self.scb = selectedCallBack

	def tableview_did_select(self, tableview, section, row):
		section_key = self.elements.keys()[section]
		self.scb(self.elements[section_key][row])
		
	def tableview_title_for_header(self, tableview, section):
		return self.elements.keys()[section]

	def tableview_number_of_sections(self, tableview):
		return len(self.elements)

	def tableview_number_of_rows(self, tableview, section):
		return len(self.elements[self.elements.keys()[section]])
		
	def tableview_cell_for_row(self, tableview, section, row):
		section_key = self.elements.keys()[section]
		try:
			cell = ui.TableViewCell('subtitle')
			cell.text_label.text = self.elements[section_key][row].get_title()
			cell.detail_text_label.text = self.elements[section_key][row].get_description()
			cell.image_view.image = ui.Image.named(self.elements[section_key][row].get_icon())
			cell.selectable = True
			return cell
		except:
			cell = ui.TableViewCell('subtitle')
			cell.text_label.text = self.elements[section_key][row].get_title()
			cell.detail_text_label.text = 'Is invalid please check file in elements folder'
			cell.selectable = False
			return cell
		
def get_view(elements, cb):
	dbo = ElementListView(elements = elements, selectedCallBack = cb)
	table_view = ui.TableView()
	table_view.name = 'Elements'
	table_view.data_source = dbo
	table_view.delegate = dbo
	return table_view
	