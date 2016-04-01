# https://gist.github.com/GuyCarver/d5da6f4b29a844a5865a
import ui
from time import sleep
import editor
import types
import console

'''
This script runs ok forever if it's the only script you run.
Other scripts may also be run if you only run this one once.
But if you run this 2 or more times any other script you try to run thereafter will lock up.
'''

templateA = [
  { 'title': 'function', 'value': 'def (  ):', 'accessory_type': 'detail_button' },
  { 'title': 'method', 'value': 'def (self):', 'accessory_type': 'detail_button' },
  { 'title': 'for', 'value': 'for i in :', 'accessory_type': 'detail_button' }, 
  { 'title': 'if', 'value': 'if ( ):', 'accessory_type': 'detail_button' },
  { 'title': 'lambda', 'value': 'lambda x: x', 'accessory_type': 'detail_button' }
  ]

#False = paste template after MyView.wait_modal(). True = paste template in MyView.picked()
pasteinview = True

#This will be bound to the DataListView object as a method after the view is loaded.
def ast(self, tv, section, row):
  #Not doing anything in here at the moment.
  #Call parent method to get MyView.info() to be called.
  ui.ListDataSource.tableview_accessory_button_tapped(self, tv, section, row)

class MyView (ui.View):
  def __init__(self):
    #Create a ListDataSource to control our list.
    lds = ui.ListDataSource(templateA)
    #override accessory button processing with a new method.
    lds.tableview_accessory_button_tapped = types.MethodType(ast, lds)
    lds.action = self.picked
    lds.accessory_action = self.info
    #Create a table view to display our list.
    tv = ui.TableView()
    tv.data_source = lds
    tv.delegate = lds
    tv.width = 250
    tv.height = tv.row_height * len(lds.items)
    
    self.add_subview(tv)
    self.width = tv.width
    self.height = tv.height
    #Easy accessors the added TableView
    self.tv = tv
    self.val = None #Set when an item if picked.

  def paste(self):
    if self.val :
      sel = editor.get_selection()
      editor.replace_text(sel[0], sel[1], self.val)
    
  def picked(self, ds):
    itm = ds.items[ds.selected_row]
    self.val = itm['value']
    if pasteinview:
      self.paste()
    self.close()
    
  def info(self, ds):
    tvc = ds.tableview_cell_for_row(self.tv, 0, ds.tapped_accessory_row)
    itm = ds.items[ds.tapped_accessory_row]
    val = itm['value']
    #Use hud_alert to display the value because detail_text_label is always None.
    console.hud_alert(val)
    if (tvc.detail_text_label):
      tvc.detail_text_label.text = val

v = MyView()
v.present('popover')
#paste in this thread.
if not pasteinview :
  while not v.on_screen :
    sleep(0.01) #Wait for view to be on screen so wait_modal will work.
  v.wait_modal() #Wait for selection to be made.  Would be nice if this took a timout value.
  v.paste()