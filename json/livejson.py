# https://forum.omz-software.com/topic/3483/livejson-webmaster4o-tuples/9

import ui
import datetime
import shelve

_themes = ['Dawn', 'Tomorrow', 'Solarized Light',
'Solarized Dark', 'Cool Glow', 'Gold', 'Tomorrow Night', 'Oceanic',
'Editorial']

d = \
    {
        'frame': (10, 10, 100, 32),
        'bg_color': 'purple',
        'tint_color' : 'white',
        'border_width':.5,
        'title': 'HELLO',
        'corner_radius':3,
        'font': ('Avenir Next Condensed', 22),
    }

dob = datetime.date(1964, 12, 17)
me = \
    {
        'DOB':dob,
    }
def make_btn(**kwargs):
	btn = ui.Button(name = 'btn')
	for k, v in kwargs.items():
		if hasattr(btn, k):
			setattr(btn, k, v)
			
	return btn
	
class ShelveObject(object):
	def __init__(self, fspec, *args, **kwargs):
		self.fspec = fspec
		self.db = None
		self.open()
		
	def open(self):
		self.db = shelve.open(self.fspec, flag='c', protocol=None, writeback=False)
		
	def set(self, key, data):
		self.db[key] = data
		
	def get(self, key):
		return self.db.get(key)
		
	def clear(self):
		self.db.clear()
		
	def close(self):
		self.db.close()
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	# open the database. 3 files are created - .dat, .dir and .bak
	so = ShelveObject('ij_test')
	so.set('themes', _themes)
	t = so.get('themes')
	x = dict(d)
	so.set('std_btn', x)
	print(t, type(t), len(t))
	for th in t:
		print(th)
		
	print(so.get('std_btn'))
	
	mc = MyClass(frame = f, bg_color = 'white')
	
	# create ui.Button using saved dict, called 'std_btn'
	btn = make_btn(**so.get('std_btn'))
	
	mc.add_subview(btn)
	mc.present('sheet', animated = False)
	
	so.set('ian', me)
	print(so.get('ian'))
	for k in so.db.keys():
		print(k)
		
	so.close()

