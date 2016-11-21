# https://forum.omz-software.com/topic/3661/populating-tableview-made-in-the-designer-from-a-list

import ui
data =['spam', 'ham', 'egg']
datasource = ui.ListDataSource(data)

view = ui.load_view('ListViewSimple2')
view.delegate = datasource

view['tableview1'].data_source=datasource
view['tableview1'].delegate=datasource

nav = ui.NavigationView(view)
nav.present()


