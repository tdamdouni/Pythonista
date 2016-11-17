# coding: utf-8

# https://github.com/cclauss/Ten-lines-or-less/blob/master/MonthView.py

# See: https://forum.omz-software.com/topic/2953/calendar-view-class

import calendar, datetime, ui

class MonthView(ui.View):
	def __init__(self, in_date=None):
		self.name = '{0:%B %Y}'.format(in_date)
		self.add_subview(ui.TextView(name='text_view', frame=(0, 0, 4096, 4096)))
		self['text_view'].editable = False
		self['text_view'].font = ('Courier New', ui.get_screen_size().w / 12.25)
		self['text_view'].text = calendar.TextCalendar().formatmonth(in_date.year, in_date.month)
		self.present()
		
MonthView(datetime.date.today())

