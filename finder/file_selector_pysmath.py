# coding: utf-8

# https://github.com/pysmath/pythonista_utilities

import ui
import os.path
import os
import clipboard

def loadFolder(sender):
	selection = sender.items[sender.selected_row]
	path = os.path.join(sender.path, selection)
	if os.path.isdir(path): # Go a level deeper in the folder tree
		new_view = ui.TableView()
		new_view.width = width
		new_view.height = height
		new_view.name = selection
		new_data = ui.ListDataSource(os.listdir(path))
		new_data.action = loadFolder
		new_data.path = path
		new_view.data_source = new_data
		new_view.delegate = new_data
		main.push_view(new_view)
	else:
		main.close()
		clipboard.set(path)
		return path
		
width = 400
height = 400
home_dir = os.path.expanduser('~/Documents/')

top = ui.TableView()
top.width = width
top.height = height
top.name = '~/Documents'

top_data = ui.ListDataSource(os.listdir(home_dir))
top_data.action = loadFolder
top_data.path = home_dir

top.data_source = top_data
top.delegate = top_data

main = ui.NavigationView(top)
main.width = width
main.height = height

main.present('sheet')

