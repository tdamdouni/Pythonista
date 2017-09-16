# https://forum.omz-software.com/topic/4328/modules-of-pythonista-displayed-with-help/5

import ui
from random import choice
from faker import Faker
fake = Faker()

# if you want random data each time this is run, comment out the line below.
fake.seed(2017)


def generate_fake_names(num_names):
	'''
	use faker module to generate a list fake first & last names
	'''
	return ['{} {}'.format(fake.first_name(), fake.last_name())
	for _ in range(num_names)]
	
	
class MyClass(ui.View):
	def __init__(self, items=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tf = None
		self.items = items if items else []
		self.table = None
		self.make_view()
		
	def make_view(self):
		_v_gap = 5
		
		# make a textfield
		tf = ui.TextField(frame=self.bounds.inset(5, 5), flex='w',
		placeholder='Filter', clear_button_mode='always',
		autocapitalization=ui.AUTOCAPITALIZE_NONE,
		spellchecking_type=False
		)
		
		tf.height = 32
		tf.delegate = self
		self.tf = tf
		self.add_subview(tf)
		
		# make a table
		tbl = ui.TableView(frame=self.bounds.inset(5, 5),
		corner_radius=3, flex='wh')
		tbl.y = tf.frame.max_y + _v_gap
		tbl.height = self.height - tf.frame.max_y - _v_gap * 2
		
		# -- Add a ui.ListDataSource
		tbl.data_source = ui.ListDataSource(self.items)
		self.table = tbl
		self.add_subview(tbl)
		
	def textfield_did_change(self, textfield):
		self.filter_data(textfield.text)
		
	def filter_data(self, filter_text=''):
		ft = filter_text.lower()
		if not len(ft):
			self.table.data_source.items = self.items
		else:
			self.table.data_source.items =\
			[s for s in self.items if ft in s.lower()]
			
if __name__ == '__main__':
	style = choice(['sheet', '', 'popover', 'panel', 'sidebar'])
	# style = 'sheet'
	f = (0, 0, 300, 400)
	v = MyClass(frame=f, items=(generate_fake_names(100)),
	bg_color='teal', name=style)
	v.present(style=style, animated=False)

