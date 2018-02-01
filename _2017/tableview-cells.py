class tvDelegate(object): #also acts as the data_source.  Can be separate, but this is easier.
	def __init__(self,items):
		#self.items = items
		self.items = items or [] 
		self.currentNumLines = len(items)
		self.currentTitle = None
		self.currentRow = None
		
	def tableview_did_select(self, tableview, section, row):
		# Called when a row was selected.
		self.currentTitle = self.items[row]['title']
		self.currentRow = row # needed for the test above
		if self.items[row]['mediaType'] == 'photo':
			preview = v['view1']
			photo = previewPhoto
			photo.image = self.items[row]['itemURL']
			preview.add_subview(photo)
			photo.frame = preview.bounds
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
		return self.currentNumLines #needed to be in sync with displayedt version,
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.background_color = '#606060'
		cell.text_label.text =  self.items[row]['title']
		if self.items[row]['mediaType'] == 'photo':
			try:
				cell.image_view.image = self.items[row]['itemURL']
			except AttributeError:
				pass
		return cell
		
	def tableview_title_for_delete_button(self, tableview, section, row):
		# Return the title for the 'swipe-to-***' button.
		return 'Delete' # or 'bye bye' or 'begone!!!'
		
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

