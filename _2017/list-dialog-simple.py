# https://forum.omz-software.com/topic/4340/share-list-dialog-simple

import ui

'''
ui.ListDataSource = LDS

Very crude example of a list dialog.
Just to show how easy it can be if you have very simple needs.
last_name is intentionally not displayed. LDS only knows about title,
image and accessory_type.
But the fact the dict contains other keys is not an issue.
'''


def show_list_dialog(items=None, *args, **kwargs):
	'''
	depending on your needs this could be your list dialog, you
	use over and over, although you would not because dialogs
	module has one already.
	'''
	items = items or []  # hmmmm thanks @ccc
	tbl = ui.TableView(**kwargs)
	tbl.data_source = ui.ListDataSource(items)
	
	# i used this because I could not get nonlocal working
	# as I thought it should work, i wanted to just use my_sel = None
	my_sel = {'value': None}
	
	class MyTableViewDelegate (object):
		# nonlocal my_sel (does not work as I understand it should)
		def tableview_did_select(self, tableview, section, row):
			my_sel['value'] = tableview.data_source.items[row]
			tableview.close()
			
	tbl.delegate = MyTableViewDelegate()
	
	tbl.present(style='sheet')
	tbl.wait_modal()  # This method is what makes this a dialog(modal)
	return my_sel['value']
	
if __name__ == '__main__':
	f = (0, 0, 400, 300)
	
	items = [{'title': 'Ian', 'last_name': "Jones"},
	{'title': 'Christian', 'last_name': "Smith"}]
	# uncomment the line below, to see the difference
	# items = ['Ian', 'John', 'Paul', 'Ringo']
	result = show_list_dialog(items, frame=f, name='Select a Name')
	print(result)
# --------------------

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
# --------------------

