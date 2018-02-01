# https://forum.omz-software.com/topic/4340/share-list-dialog-simple/2

import ui

def show_list_dialog(items=None, *args, **kwargs):
	items = items or []  # hmmmm thanks @ccc
	tbl = ui.TableView(**kwargs)
	tbl.data_source = ui.ListDataSource(items)
	
	selection = None
	
	class MyTableViewDelegate (object):
		def tableview_did_select(self, tableview, section, row):
			nonlocal selection
			selection = tableview.data_source.items[row]
			tableview.close()
			
	tbl.delegate = MyTableViewDelegate()
	
	tbl.present(style='sheet')
	tbl.wait_modal()  # This method is what makes this a dialog(modal)
	return selection
	
if __name__ == '__main__':
	f = (0, 0, 400, 300)
	
	items = [{'title': 'Ian', 'last_name': "Jones"},
	{'title': 'Christian', 'last_name': "Smith"}]
	# uncomment the line below, to see the difference
	# items = ['Ian', 'John', 'Paul', 'Ringo']
	result = show_list_dialog(items, frame=f, name='Select a Name')
	print(result)

