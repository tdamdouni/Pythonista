# https://forum.omz-software.com/topic/1869/ui-on-desktop/15

# Putting list into a multiple selection Pythonista ui is easy and requires no Swift...

import ui
my_list = [x for x in 'abcdefghijklmnopqrstuvwxyz']
view = ui.TableView(name='My List')
view.allows_multiple_selection = True
view.data_source = ui.ListDataSource(my_list)
view.present()
