# coding: utf-8

# https://forum.omz-software.com/topic/1524/simple-demo-of-tableview-logic-for-the-novices

# https://forum.omz-software.com/topic/4261/using-delete-in-ui-tableview/2

# and example of tableview and how to control/use them

import ui,console

def listShuffle(list,row_from, row_to):
	''' a method to re-order a list '''
	from_item = list[row_from]
	del list[row_from]
	list.insert(row_to,from_item)
	return list
	
class tvDelegate(object): #also acts as the data_source.  Can be separate, but this is easier.
	def __init__(self,items):
		self.items = items
		self.currentNumLines = len(items)
		self.currentTitle = None
		self.currentRow = None
		
	def tableview_did_select(self, tableview, section, row):
		# Called when a row was selected.
		try:
			self.items[self.currentRow]['accessory_type'] = 'none' # un-flags current selected row
		except TypeError: #needed for very first selection
			pass
		self.items[row]['accessory_type']  = 'checkmark'
		self.currentTitle = self.items[row]['title']
		self.currentRow = row # needed for the test above
		tableview.reload_data() # forces changes into the displayed list
		
		
	def tableview_did_deselect(self, tableview, section, row):
		# Called when a row was de-selected (in multiple selection mode).
		pass
		
	def tableview_title_for_delete_button(self, tableview, section, row):
		# Return the title for the 'swipe-to-***' button.
		return 'Delete' # or 'bye bye' or 'begone!!!'
		
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1). Someone else can mess with
		# sections and section logic
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return self.currentNumLines #needed to be in sync with displayed version,
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text =  self.items[row]['title']
		cell.accessory_type = self.items[row]['accessory_type']
		# or you could comment out the line above and use
		#
		#if self.items[row]['accessory_type'] == 'checkmark':
		#   cell.text_label.font = ('<system-bold>',20)
		# or
		# cell.text_label.text_color = '#FF0000'
		#
		# for emphasis instead
		#
		return cell
		
		
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return True # you can use logic to lock out specific ("pinned" entries)
		
	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return True # see above
		
	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		self.currentNumLines -=1 # see above regarding hte "syncing"
		tableview.delete_rows((row,)) # this animates the deletion  could also 'tableview.reload_data()'
		del self.items[row]
		
	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		# Called when the user moves a row with the reordering control (in editing mode).
		
		self.items = listShuffle(self.items,from_row,to_row)
		# cynchronizes what is displayed with the underlying list
		
def onEdit(sender):
	global tv
	tv.editing = True
	
	
def onDone(sender):
	global tv
	tv.editing = False
	# to avoid consufion in the selection logic, I clear all accessory type after an edit.
	for row in range(len(tv.data_source.items)):
		tv.data_source.items[row]['accessory_type'] = 'none'
	tv.reload_data()
	
titles = "one two three four five six seven eight".split()
itemlist = [{'title': x, 'accessory_type':'none'} for x in titles]

vdel = tvDelegate(items=itemlist)

#the pyui file consists of a tableview named tv_1
#and two buttons named button1 and button2 with labels 'edit' and 'done' respectively


v = ui.load_view()
tv = v['tv_1']
v['button1'].action = onEdit
v['button2'].action = onDone
tv.delegate = tv.data_source = vdel
v.present('sheet')

