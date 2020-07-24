# coding: utf-8

# https://gist.github.com/Phuket2/ecb60f488de9da299c7b

from __future__ import print_function
import ui
from collections import namedtuple
import string

MainRec = namedtuple('MainRec', 'title,image,accessory_type')

_interface_bg = 'navy'
_interface_text_color = 'black'



def get_recs(nb_recs)   :
	lst = []
	for i in range(nb_recs):
		x = MainRec(title = str(i), image = None, accessory_type = 'disclosure_indicator')
		lst.append(x._asdict())
	return lst



class DetailView(ui.View):
	def __init__(self, parent):
		self.parent = parent

		#self.flex = 'wh'
		self.bg_color = 'white'
		#self.border_width = 5
		#self.border_color = 'green'
		self.create_view()

	def create_view(self):
		pass

	def layout(self):
		self.corner_radius = 6
		r = ui.Rect(*self.bounds)
		self.frame = r



class MainView(ui.View):
	def __init__(self, parent, width_percent = .33):
		self.parent = parent

		self.bg_color = _interface_bg
		self.width_percent = width_percent
		self.table = None


		self.search = None

		self.create_view()

	def create_view(self):

		self.search = SearchView(self)


		tbl = ui.TableView()
		tbl.corner_radius = 6
		tbl.border_width = .5
		tbl.background_color = _interface_bg
		self.table = tbl
		#self.table.data_source = self
		#self.table.data_source.accessory_action =
		#self.table.data_source.action = self.parent.hit

		#main.add_subview(search)
		self.add_subview(self.table)
		self.add_subview(self.search)

	def layout(self):

		#resize ourself
		r = ui.Rect(*self.parent.bounds)
		r.width = r.width * self.width_percent
		self.frame = r

		# resize the table
		r1 = ui.Rect(*self.bounds)
		self.table.frame = r1.inset(44, 5)


		self.search.border_width = 2
		# rezize search
		self.search.y= 0
		self.search.x = 0
		self.search.width = self.width




class SearchView(ui.View):
	def __init__(self, parent):
		self.parent = parent
		self.search_field = None
		self.bg_color = _interface_bg
		self.height = 42

		self.create_view()

	def create_view(self):
		sf = ui.TextField()
		#self.search_field = ui.TextField()
		sf.corner_radius = 3
		sf.placeholder = 'Search'
		sf.alignment = ui.ALIGN_CENTER
		sf.flex = 'wh'
		sf.background_color = _interface_bg
		sf.text_color = _interface_text_color
		sf.delegate = self

		self.search_field = sf
		self.add_subview(self.search_field)

	def layout(self):
		self.search_field.frame = ui.Rect(*self.bounds).inset(8,8)

	def textfield_should_change(self, textfield, range, replacement):
		# rough test. only ascii chars, no spaces
		if not replacement :
			return True
			
		for c in str(replacement):
			if c not in string.ascii_letters:
				return False

		return True



class UiRemindersStyle (ui.View):
	def __init__(self , main_width = .33, **kwargs):
		ui.View.__init__(self, **kwargs)

		self.main_percent = main_width

		self.main = None
		self.detail = None
		self.search = None
		self.table = None
		self.main_width = 0

		#create the views
		self.create_views()

	def create_views(self):
		# create the views, dont worry about sizes yet.. do it in layout

		# create main view
		main = MainView(self, self.main_percent)
		self.main = main

		# create search view
		self.search = SearchView(self.main)
		#self.add_subview(self.search)

		self.add_subview(main)

		self.detail = DetailView(self)
		self.add_subview(self.detail)



	def layout(self):
		# main view
		r = ui.Rect(*self.bounds)
		r.width = r.width * self.main_percent
		self.main.frame = r

		r = ui.Rect(*self.bounds)
		r.width -= self.main.width
		r.x  = self.main.width

		self.detail.bounds = r.inset(10,10, 44, 0)

	def set_main_data(self, items):
		print(self.main.table)
		tbl = self.main.table
		tbl.data_source = ui.ListDataSource(items = get_recs(40))
		tbl.data_source.action = self.hit_main

	def hit_main(self, sender):
		print('inside hit callback main')
		print(sender.name)


if __name__ == '__main__':
	f = ui.Rect(0,0,768, 768)
	rem  = UiRemindersStyle(frame = f, main_width =.5, name = 'Reminders')
	rem.set_main_data(range(40))
	rem.present('sheet')