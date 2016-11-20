# coding: utf-8

# https://forum.omz-software.com/topic/1244/changing-text-color-in-table-view-cell/4

class MyDataSource(object):
	def tableview_cell_for_row(self, tv, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text_color = (1.0, 0.0, 0.0, 0.0)
		cell.text_label.text = "I am red"
		return cell
# --------------------

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = self.items[row]['title']
		if row == highlight:
			cell.text_label.text_color = 'red'
		cell.accessory_type = self.items[row]['accessory_type']
		return cell
# --------------------

