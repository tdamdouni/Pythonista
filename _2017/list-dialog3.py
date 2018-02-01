# https://forum.omz-software.com/topic/4340/share-list-dialog-simple/3

import ui


class MyDataSource(ui.ListDataSource):
	def tableview_cell_for_row(self, tv, section, row):
		item = self.items[row]
		cell = ui.TableViewCell('default')
		cell.text_label.text = '{} {}'.format(item['first_name'], item['last_name'])
		return cell
		
		
def show_list_dialog(items=None, **kwargs):
	result = None
	
	tbl = ui.TableView(**kwargs)
	tbl.data_source = MyDataSource(items or [])
	tbl.delegate = tbl.data_source
	
	def did_select(ds):
		nonlocal result
		result = ds.items[ds.selected_row]
		tbl.close()
		
	tbl.data_source.action = did_select
	tbl.present(style='sheet')
	tbl.wait_modal()
	
	return result
	
if __name__ == '__main__':
	f = (0, 0, 400, 300)
	items = [{'first_name': 'Ian', 'last_name': "Jones"},
	{'first_name': 'Christian', 'last_name': "Smith"}]
	result = show_list_dialog(items, frame=f, name='Select a Name')
	print(result)

