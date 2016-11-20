# http://codegists.com/snippet/python/pythonista-tableviewopenwithlistpy_bboyheadman_python

import ui

def show(window_title, rows):
	class MyTableViewDataSource (object):
		def tableview_cell_for_row(self, tableview, section, row):
			row_title, row_description = rows[row]
			# 'subtitle'-style cells come with a built-in secondary label
			cell = ui.TableViewCell('subtitle')
			cell.text_label.text = row_title
			cell.detail_text_label.text = row_description
			cell.detail_text_label.text_color = '#555'
			return cell
			
		def tableview_number_of_rows(self, tableview, section):
			return len(rows)
			
	tb = ui.TableView()
	tb.name = window_title
	tb.size_to_fit()
	tb.data_source = MyTableViewDataSource()
	tb.present('sheet')
	
show('Window Title', [['title', 'description'], ['title', 'description']])

