# coding: utf-8

# https://github.com/pysmath/pythonista_utilities/blob/master/save.py

from __future__ import print_function
import appex, console
import ui
import os.path
import os
import clipboard
import gc
import shutil

def loadFolder(sender): #Populate a new list view with the contents of a selected folder and push to the navigation view
    selection = sender.items[sender.selected_row]
    path = os.path.join(sender.path, selection)
    new_view = ui.TableView()
    new_view.name = selection
    new_data = ui.ListDataSource(next(os.walk(path))[1])
    new_data.action = loadFolder
    new_data.path = path
    new_view.data_source = new_data
    new_view.delegate = new_data
    sender.tableview.navigation_view.push_view(new_view)

def find_current_view(nv): #Find the currently open folder when the select button is pushed
    for v in gc.get_objects():
        if hasattr(v, 'navigation_view') and v.navigation_view == nv and not v.superview:
            return v
    return None

def makeSelection(sender): #Select the currently open folder and move on to the saving process
    current_view = find_current_view(picker).data_source.path
    picker.close()
    clipboard.set(current_view)
    return current_view

def folder_picker(): #Initialize the folder picker
    home_dir = os.getcwd().split('Documents/')[0] + 'Documents/'
    
    top = ui.TableView()
    top.name = '~/Documents'
    
    top_data = ui.ListDataSource(next(os.walk(home_dir))[1])
    top_data.action = loadFolder
    top_data.path = home_dir
    
    top.data_source = top_data
    top.delegate = top_data
    
    select_button = ui.ButtonItem(action = makeSelection, title = 'Select')
    
    main = ui.NavigationView(top)
    main.right_button_items = [select_button]
    main.current_view = home_dir
    
    return main

def save(folder):
    if appex.is_running_extension():
        sFp = appex.get_file_path()
        if sFp:
            console.hud_alert('Saving...')
            print('Destination folder: ', os.path.join(folder, os.path.basename(sFp)))
            shutil.copy(sFp, folder)
            console.hud_alert('Saved')

if __name__ == '__main__':
    picker = folder_picker()
    picker.present('sheet')
    picker.wait_modal()
    folder = clipboard.get()
    save(folder)
