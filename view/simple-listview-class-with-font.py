# https://forum.omz-software.com/topic/3597/share-simple-listview-class

# Pythonista Forum - @Phuket2
import ui, itertools
from objc_util import ObjCClass

#def get_font_list():
        # from someone on the forum, i think @omz
        #UIFont = ObjCClass('UIFont')
        #return list(itertools.chain(*[UIFont.fontNamesForFamilyName_(str(x))
        #for x in UIFont.familyNames()]))

def get_font_list():
        # from someone on the forum, i think @omz
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
		tbl.data_source.action = self.my_action
		self.tbl = tbl
		self.add_subview(tbl)
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		fnt_name = str(tableview.data_source.items[row])
		cell.text_label.text = fnt_name
		cell.text_label.font = (fnt_name, 16)
		return cell
		
	def my_action(self, sender):
		self.value = sender.items[sender.selected_row]
		self.close()
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	style = ''
	my_list = get_font_list()
	v = SimpleListView(my_list, frame=f, name='Font List')
	v.present(style=style)
	v.wait_modal()
	print(v.value)
# --------------------

