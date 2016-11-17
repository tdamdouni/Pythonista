# https://forum.omz-software.com/topic/941/tableviewcell-detail_text_label/2

import ui

class source (object):
	def tableview_number_of_rows(self, tv, s):
		return 4
		
	def tableview_cell_for_row(self, tv, s, r):
		type = {0:'default', 1:'subtitle', 2:'value1', 3:'value2'}[r]
		cell = ui.TableViewCell(type)
		cell.text_label.text = 'Title'
		try:
			cell.detail_text_label.text = 'Detail'
		except AttributeError:
			pass
		try:
			cell.image_view.image = ui.Image.named('ionicons-image-32')
		except AttributeError:
			pass
		return cell
		
view = ui.TableView()

view.data_source = source()

view.present()

