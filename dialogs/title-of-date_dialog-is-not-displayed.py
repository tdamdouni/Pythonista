#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/3059/title-of-date_dialog-is-not-displayed/3

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

