# coding: utf-8

import ui

def add_new_item(sender):
  tv1.data_source.items.append(view['new_item'].text)
  tv1.reload_data()

view = ui.load_view('shoppinglist')
view.present('sheet')
lst = ui.ListDataSource(items=[])
tv1 = view['shoppinglist']
tv1.data_source = lst
