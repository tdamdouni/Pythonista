#!/usr/bin/env python

# https://github.com/dgelessus/filenav/blob/master/litenav.py

###############################################################################
# litenav by dgelessus
# A simplified version of the original filenav. Only supports basic folder
# listing and navigation.
###############################################################################

import os  # used to navigate the file structure
import sys # for sys.argv
import ui  # duh

class FileDataSource(object):
    # ui.TableView data source that generates a directory listing
    def __init__(self, path=os.getcwd()):
        # init
        self.path = full_path(path)
        self.refresh()
        self.lists = [self.folders, self.files]

    def refresh(self):
        # Refresh the list of files and folders
        self.folders = []
        self.files = []
        for f in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, f)):
                self.folders.append(f)
            else:
                self.files.append(f)

    def tableview_number_of_sections(self, tableview):
        # Return the number of sections
        return len(self.lists)

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        return len(self.lists[section])

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        cell = ui.TableViewCell()
        cell.text_label.text = os.path.basename(os.path.join(self.path, self.lists[section][row]))
        if section == 0:
            cell.accessory_type = "disclosure_indicator"
        return cell

    def tableview_title_for_header(self, tableview, section):
        # Return a title for the given section.
        if section == 0:
            return "Folders"
        elif section == 1:
            return "Files"
        else:
            return ""
    
    def tableview_did_select(self, tableview, section, row):
        # Called when the user selects a row
        if section == 0:
            nav.push_view(make_file_list(os.path.join(self.path, self.folders[row])))
    

def close_proxy():
    def _close(sender):
        nav.close()
    return _close

def full_path(path):
    # Return absolute path with expanded ~s, input path assumed relative to cwd
    return os.path.abspath(os.path.join(os.getcwd(), os.path.expanduser(path)))

def make_file_list(path):
    # Create a ui.TableView containing a directory listing of path
    path = full_path(path)
    lst = ui.TableView(flex="WH")
    # allow multiple selection when editing, single selection otherwise
    lst.allows_selection = True
    lst.allows_multiple_selection = False
    lst.background_color = 1.0
    lst.data_source = lst.delegate = FileDataSource(path)
    lst.name = os.path.basename(path)
    current_list = lst
    return lst

if __name__ == "__main__":
    lst = make_file_list("~")
    lst.left_button_items = ui.ButtonItem(image=ui.Image.named("ionicons-close-24"), action=close_proxy()),

    nav = ui.NavigationView(lst)
    nav.navigation_bar_hidden = False
    nav.name = "LiteNav"
    nav.flex = "WH"
    nav.height = 1000
    
    nav.present("popover", hide_title_bar=True)
