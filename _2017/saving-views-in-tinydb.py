# https://forum.omz-software.com/topic/4245/tinydb-request-for-pythonista/9

import ui

try:
	from tinydb import TinyDB, Query, __version__ as tinydb_version
except ImportError:
	print('tinydb v3.4.1 or greater needs to be insalled to run this app')
	exit(1)
	
	
def save_view(filename, key, jstr):
	'''
	save or update the json str of a view into the database with a key.
	The key, is how we recover the view later
	'''
	db = TinyDB(filename)
	
	el = db.get(Query()['key'] == key)
	pay_load = {'key': key, 'data': jstr}
	
	if el:
		db.update(pay_load, eids=[el.eid])
		print('Updated View-{}'.format(key))
	else:
		db.insert(pay_load)
		print('Created View-{}'.format(key))
		
		
def get_saved_view(filename, key):
	'''
	return a ui.View given a key that has been previously saved to
	the database.
	'''
	db = TinyDB(filename)
	el = db.get(Query()['key'] == key)
	if el:
		return ui.load_view_str(el['data'])
		
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		pass
		
		
class MyClass2(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		pass
		
if __name__ == '__main__':
	db_filename = 'myviews.json'
	f = (0, 0, 300, 400)
	v = MyClass(frame=f)
	v.present(style='sheet', animated=False)
	
	v2 = MyClass2(name='MyClass2', bg_color='purple', frame=f)
	
	save_view(db_filename, 'myClass', ui.dump_view(MyClass()))
	save_view(db_filename, 'myClass2', ui.dump_view(v2))
	
	v3 = get_saved_view(db_filename, key='myClass2')
	v3.present('sheet')
	v3.wait_modal()
	v3.bg_color = 'orange'
	v3.title = 'Orange View'
	v3.add_subview(ui.DatePicker())
	save_view(db_filename, 'myClass2', ui.dump_view(v3))
	v4 = get_saved_view(db_filename, key='myClass2')
	v4.present('sheet')

