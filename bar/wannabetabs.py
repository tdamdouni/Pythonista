# -*- coding: utf-8 -*-
###############################################################################
# wannabetabs by dgelessus
###############################################################################

import editor
import os
import ui

def full_path(path):
	# Return absolute path with expanded ~ and symlinks, input path assumed relative to cwd
	return os.path.realpath(os.path.abspath(os.path.expanduser(path)))
	
def current_path():
	# path to file currently open in editor
	return "/private" + editor.get_path()
	
def current_relpath():
	# like current_path, but relative to Script Library
	return os.path.relpath(current_path(), os.path.expanduser("~/Documents"))
	
def tb_button_action(sender):
	# generic action for toolbar buttons
	if sender in tab_list.left_button_items:
		root_view.close()
	elif sender in tab_list.right_button_items:
		if sender.title == "Edit":
			tab_list.set_editing(True)
			sender.title = "Done"
		elif sender.title == "Done":
			tab_list.set_editing(False)
			sender.title = "Edit"
		elif sender == tab_list.right_button_items[2]:
			tab_set = set(tab_ds.items)
			tab_set.add(current_relpath())
			tab_ds.items = list(tab_set)
			
def ds_action(sender):
	# generic action for data source
	if sender.selected_row >= 0:
		editor.open_file(sender.items[sender.selected_row])
		
if __name__ == "__main__":
	tab_set = set([current_relpath()])
	
	root_view = ui.View(flex="WH")
	root_view.width = 200
	root_view.border_color = 0.7
	root_view.border_width = 1
	
	tab_ds = ui.ListDataSource(list(tab_set))
	tab_ds.delete_enabled = True
	tab_ds.move_enabled = True
	tab_ds.action = ds_action
	
	tab_list = ui.TableView(flex="WH")
	tab_list.data_source = tab_ds
	tab_list.delegate = tab_ds
	tab_list.left_button_items = ui.ButtonItem(title="    ", action=tb_button_action),
	tab_list.right_button_items = (ui.ButtonItem(title="    ", action=tb_button_action), ui.ButtonItem(title="Edit", action=tb_button_action), ui.ButtonItem(image=ui.Image.named("ionicons-ios7-plus-empty-32"), action=tb_button_action))
	
	nav = ui.NavigationView(tab_list, flex="WH")
	nav.navigation_bar_hidden = False
	
	root_view.add_subview(nav)
	
	root_view.present("sidebar")
	
	nav.width = root_view.width
	nav.height = root_view.height

