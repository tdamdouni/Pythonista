# https://forum.omz-software.com/topic/3593/simple-n00b-question-populating-tableview-from-a-list

import ui
data = [x for x in range(0, 50)]
datasource = ui.ListDataSource(data)
tv = ui.TableView()
tv.data_source = datasource
tv.delegate = datasource

def selectitem(*args):
	view = ui.View(title='{}'.format(args[1]))
	label = ui.Label()
	label.text = "{}, {}, {}".format(*args)
	label.size_to_fit()
	view.add_subview(label)
	view.background_color = 'white'
	nav.push_view(view)
datasource.tableview_did_select = selectitem

nav = ui.NavigationView(tv)

nav.present()
# --------------------
import dialogs

def show_dlg(the_list):
	return dialogs.list_dialog('Please select', the_list)
	
	
lst = range(100)
res=show_dlg(lst)
print(res)
# --------------------

