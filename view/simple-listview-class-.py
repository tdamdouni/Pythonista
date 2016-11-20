# https://forum.omz-software.com/topic/3597/share-simple-listview-class/12

# Pythonista Forum - @Phuket2
import ui, clipboard, console
from objc_util import *

def get_font_list():
	# updated version from @dgelessus
	UIFont = ObjCClass('UIFont')
	lst = [str(font) for family in UIFont.familyNames() for font in
	UIFont.fontNamesForFamilyName_(family)]
	lst.sort()
	return lst
	
class SimpleListView(ui.View):
	def __init__(self, items, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tbl = None
		self.value = None
		self.flex = 'wh'
		
		self.make_view(items)
		
	def make_view(self, items):
		tbl = ui.TableView(frame=self.bounds)
		tbl.flex = 'wh'
		tbl.data_source = tbl.delegate = ui.ListDataSource(items)
		tbl.data_source.tableview_cell_for_row =\
		self.tableview_cell_for_row
		
		self.tbl = tbl
		self.add_subview(tbl)
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		data = tableview.data_source.items[row]
		cell.text_label.text = data
		cell.text_label.font = (data,  16)
		return cell
		
class FontViewer(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.data = get_font_list()
		self.tbl = None
		self.bg_color = 'darkgray'
		self.flex = 'wh'
		self.name_str = self.name if self.name else 'Fonts'
		
		self.make_view(**kwargs)
		self.update_name()
		
	def make_view(self, **kwargs):
		# make the containing view
		margin = kwargs.pop('margin', (0, 0))
		cv = ui.View(frame=self.bounds.inset(*margin))
		cv.flex = 'wh'
		
		# make the search view
		sv = ui.View(frame=cv.bounds)
		sv.height = 32
		tv = ui.TextField(frame=sv.bounds)
		tv.placeholder = 'search'
		tv.clear_button_mode = 'always'
		tv.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
		tv.autocorrection_type = False
		tv.delegate = self
		tv.flex = 'wh'
		sv.add_subview(tv)
		sv.flex = 'w'
		cv.add_subview(sv)
		
		# make the list view
		lv = ui.View(frame=sv.frame)
		lv.height = cv.height - sv.frame.max_y - 5
		lv.y = sv.frame.max_y + 5
		lv.corner_radius = 6
		
		lv.flex = 'wh'
		cv.add_subview(lv)
		
		# create the list
		slv = SimpleListView(self.data, frame=f)
		self.tbl = slv.tbl
		
		# redirect the action to this class.
		self.tbl.data_source.action = self.list_action
		lv.add_subview(slv)
		
		self.add_subview(cv)
		
	def textfield_did_change(self, textfield):
		self.filter_data(textfield.text)
		
	def filter_data(self, filter_txt):
		# real poor mans filter.  just doing an in-string search to match
		# but its case insensitive. for this data seems reasonable.
		txt = filter_txt.lower()
		
		# ui.ListDataSource updates itself when the items are changed
		self.tbl.data_source.items = [item for item in self.data
		if txt in item.lower()]
		self.update_name()
		
	def update_name(self):
		self.name = '{} - ({})'.format(self.name_str,
		len(self.tbl.data_source.items))
		
	def list_action(self, sender):
		# when a list item is clicked
		self.value = sender.items[sender.selected_row]
		clipboard.set(self.value)
		console.hud_alert('{} - copied'.format(self.value))
		self.close()
		
if __name__ == '__main__':
	w, h = 400, 800
	style = 'popover'
	if style == 'popover':
		h = ui.get_screen_size()[1] * .6
		
	f = (0, 0, w, h)
	
	fv = FontViewer(name='The Fonts', frame=f, margin=(5, 5))
	fv.present(style=style)

