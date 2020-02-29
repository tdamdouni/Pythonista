#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/3059/title-of-date_dialog-is-not-displayed/8

from __future__ import print_function
import ui
import datetime


class CustomDatePicker(ui.View):
	def __init__(self, date = None, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		self.date = date
		self.dp = None
		
		self.make_view()
		
		m_btn = ui.ButtonItem(title = 'Select')
		m_btn.action = self.hit
		self.right_button_items = (m_btn, )
		
	def make_view(self):
		obj = ui.DatePicker(name = 'dp')
		if self.date:
			obj.date = self.date
		obj.mode = ui.DATE_PICKER_MODE_DATE
		obj.frame = self.frame
		obj.flex = 'WH'
		self.add_subview(obj)
		self.dp = obj
		
	def hit(self, sender):
		self.close()
		
if __name__ == '__main__':
	f = (0, 0, 400, 300)
	d = datetime.datetime.now()
	d += datetime.timedelta(days  = -7 )
	cdp = CustomDatePicker(frame = f , bg_color = 'orange', date = d, name ='Please select a date')
	cdp.present('sheet')
	cdp.wait_modal()
	print(cdp.dp.date)
	
# --------------------

# coding: utf-8

import ui
import datetime


class CustomDatePicker(ui.View):
	def __init__(self, date = None, *args, **kwargs):
		#ui.View.__init__(self, *args, **kwargs)
		self.date = date
		self.dp = None
		
		self.handle_kwargs(**kwargs)
		self.make_view()
		
		m_btn = ui.ButtonItem(title = 'Select')
		m_btn.action = self.hit
		self.right_button_items = (m_btn, )
		
	def handle_kwargs(self, **kwargs):
		for k, v in kwargs.iteritems():
			if hasattr(self, k):
				setattr(self, k, v)
				
	def make_view(self):
		obj = ui.DatePicker(name = 'dp')
		if self.date:
			obj.date = self.date
			
		obj.frame = self.frame
		obj.mode = ui.DATE_PICKER_MODE_DATE
		obj.flex = 'WH'
		self.add_subview(obj)
		self.dp = obj
		
	def hit(self, sender):
		self.close()
		
if __name__ == '__main__':
	f = (0, 0, 400, 300)
	d = datetime.datetime.now()
	d += datetime.timedelta(days  = -7 )
	cdp = CustomDatePicker(frame = f , bg_color = 'orange', date = d, name ='Please select a date')
	cdp.present('sheet')
	cdp.wait_modal()
	print(cdp.dp.date)
	
# --------------------

class _DateDialogController (object):
	def __init__(self, mode=ui.DATE_PICKER_MODE_DATE, title='', done_button_title='Done'):
		self.was_canceled = True
		self.container_view = ui.View(background_color='white')
		self.view = ui.DatePicker()
		self.container_view.name = title
		self.view.mode = mode
		self.view.background_color = 'white'
		self.view.frame = (0, 0, 500, 500)
		self.view.flex = 'WH'
		self.container_view.frame = self.view.frame
		self.container_view.add_subview(self.view)
		
# --------------------

import ui

dp = ui.DatePicker(name = 'test')
dp.present('sheet')

# --------------------

