# https://forum.omz-software.com/topic/3597/share-simple-listview-class

# Pythonista Forum - @Phuket2
import ui, itertools
from objc_util import ObjCClass

def get_font_list():
	# from someone on the forum, i think @omz
	UIFont = ObjCClass('UIFont')
	return list(itertools.chain(*[UIFont.fontNamesForFamilyName_(str(x))
	for x in UIFont.familyNames()]))
	
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
		tbl.data_source.action = self.my_action
		self.tbl = tbl
		self.add_subview(tbl)
		
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

