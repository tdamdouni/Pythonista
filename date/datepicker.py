# https://gist.github.com/Phuket2/7e7bba9276262e683c4741a3ceabf690

import ui, editor
import calendar
from datetime import datetime, timedelta
import time
from datetime import date as Date
c = calendar.Calendar()


# seems like a good idea, mostly. But feels it should have a stronger 
# framework around it. The basic concept seems to be ok though. But, 
# i am not good enough to think about the 1 billion possible side effects
def raise_event(sender, event_handler = None, **kwargs):
	sv=sender.superview
	
	if not event_handler:
		if not hasattr(sender, 'event_handler'):
			return
		else:
			event_handler = sender.event_handler
					
	handler = event_handler
	# walk up view chain to find callable action_name
	while sv:
		a=getattr(sv, handler, None)
		if callable(a):
			result = a(sender, **kwargs)
			# fix the code below
			if type(result) is bool:
				if result: return
			else:
				return result
		sv=sv.superview
	return
	
	
# added this after.. yeah a after thought...
class ModelCalender(object):
	'''
		Data Model
		Calendar 
	'''
	def __init__(self, d= None, first_day_week = calendar.SUNDAY):
		'''
		-->In:
			d = date, if None d is set to Todays date
			fdow = first day of the week
		<--Out:
			None
		'''
		self.cal = calendar.Calendar(first_day_week)
		calendar.setfirstweekday(first_day_week)
		self.date = d
		if not self.date:
			self.date = Date.today()
	
	@staticmethod
	def weekday_header():
		return [day for day in calendar.weekheader(3).split(' ')]

	def get_dates_for_month(self, year, month):
		'''
			Returns - list
			Contents - datetime objects
			Scope - 
			returns a list of datetime obj for a month. provides prev and
			next days for a month block. i.e 7cols x 5 Rows
			Notes - super handy function from calendar.Calendar
		'''
		return [dt for dt in self.cal.itermonthdates(year, month)]
	
	def get_next_month(self):
		d = self.date
		dt = Date(d.year, d.month, self.days_in_month(d)) +\
						timedelta(days = 1)
		self.date = dt
		return dt
		
	def get_prev_month(self):
		d = self.date
		dt = Date(d.year, d.month, 1) - timedelta(days = 1)
		self.date = dt
		return dt
		
	@staticmethod
	def is_today(dt):
		# returns a boolean , dt == today
		today = Date.today()
		return (dt.year, dt.month, dt.day) ==\
				(today.year, today.month, today.day)
				
	@staticmethod			
	def is_same_month(d1, d2):
		# returns boolean if year and month are the same for d1 and d2
		return (d1.year, d1.month) == (d2.year, d2.month)
		
	def month_year_str(self, dt=None, abbr = False):
		if not dt: dt = self.date
		m_name = calendar.month_name[dt.month] if not abbr else\
				calendar.month_abbr[dt.month]

		return '{month}, {year}'.format(month = m_name, year = dt.year)
		
	@staticmethod
	def days_in_month(dt):
		return calendar.monthrange(dt.year, dt.month)[1]
	
	def help(self):
		print(help(self))

def get_dates_for_month(year, month):
	# returns a list of dates for a month. provides previous and
	# following days for a month block. i.e 7cols x 5 Rows
	# super handy function from calendar.Calendar
	return [d for d in c.itermonthdates(year, month)]



def make_cal_button(idx , action):
	btn = ui.Button(frame = (0, 0, 100, 100))
	btn.border_width = .5

	btn.action = action
	btn.date = None
	btn.select = True
	btn.idx = idx
	lb = ui.Label(frame = btn.frame)
	lb.alignment = ui.ALIGN_CENTER
	#lb.font = CalSettings.day_font
	#lb.text_color = CalSettings.day_text_color
	btn.add_subview(lb)
	btn.day_lb = lb
	
	return btn
	
def get_css_color(color_name, alpha = 1.0):
	'''
		A simple util to return a tuple (RGBA) given a css name
	'''
	c = ui.parse_color(color_name)
	return (c[0],c[1], c[2], alpha)
	
class TitleBar(ui.View):
	def __init__(self, fixed_h = 44,  *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fixed_h = fixed_h
		
		self.lb = None			
		self.make_view()
		
	def make_view(self):
		self.frame = (0, 0, self.width, self.fixed_h)
		self.border_width = .5
		#self.bg_color = 'lightblue'
		
		lb = ui.Label()
		lb.alignment = ui.ALIGN_CENTER	
		lb.frame = self.bounds
		self.lb = lb
		self.add_subview(self.lb)
		
		btn = ui.Button(name ='prev', frame = (0, 0, 32, 32))
		btn.image = ui.Image.named('iob:arrow_left_a_32')
		
		btn.event_handler  = 'goto_prev_month'
		btn.action = raise_event
		self.add_subview(btn)
		
		btn = ui.Button(name ='next', frame = (0, 0, 32, 32))
		btn.image = ui.Image.named('iob:arrow_right_a_32')
		btn.event_handler = 'goto_next_month'
		btn.action = raise_event
		self.add_subview(btn)
			
		
	def layout(self):
		sv = self.superview
		if not sv: return
		
		self.width = sv.bounds.width
		self.height = self.fixed_h
		
		self.lb.width = self.width
		self.lb.center = self.center
		
		self['prev'].center = self.center
		self['prev'].x = 10
		
		self['next'].center = self.center
		self['next'].x = self.bounds.max_x - 10 - self['next'].width
	

	
	def set_date_title(self, date):
		self.lb.text = '{month}, {year}'.format(month = calendar.month_name[date.month], year = date.year)
	
	@property
	def title_label(self):
		return self.lb
			
class DaysHeader(ui.View):
	def __init__(self, bar_h = 44,  *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.bar_h = 44
		self.data = None
		self.make_view()
		
	def make_view(self):
		self.frame = (0, 0, self.bounds.width, 44)
		#for i, d in enumerate(calendar.weekheader(3).split(' ')):
		for i in range(7):
			lb = ui.Label(name = str(i))
			lb.text = str(i)
			lb.alignment = ui.ALIGN_CENTER
			self.add_subview(lb)
	
	# would be great to have the did_load callback for custom views as
	# well as pyui/UIFiles. 
	'''		
	def did_load(self):
		# query the data
	'''
			
	def layout(self):
		sv = self.superview
		if not sv: return
		
		# yeah, this is strange. but if had did_load callback for 
		# custom ui.Views, could handle data loading there
		# this is very sloppy, i know
		if not self.data:
			self.data = self.get_data()
			for i, lb in enumerate(self.subviews):
				lb.text =self.data[i]
			
		self.width = sv.bounds.width
		
		w = self.width / 7 
		h = self.bar_h
		
		# labels in the subview, to display the day names
		for i, sv in enumerate(self.subviews):
			sv.frame = (i * w, 0, w, h)
		
	# oh my god... send a message to the universe to give me some data
	def get_data(self):
		return raise_event(self, 'week_header_data_get')
		

class ToolBar(ui.View):
	def __init__(self, bar_h = 44,  *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.bar_h = bar_h
		self.make_view()
		
	def make_view(self):
		self.frame = (0, 0, self.width, self.bar_h)
		
		# Today button
		btn = ui.Button(name = 'today')	
		btn.title = 'TODAY'
		btn.size_to_fit()
		# size_to_fit a little tight, should have a margin param
		btn.width *= 1.5
		btn.event_handler = 'goto_today'
		btn.action = raise_event
		self.add_subview(btn)
		
		# Cancel button
		btn = ui.Button(name = 'cancel')	
		btn.title = 'CANCEL'
		btn.size_to_fit()
		btn.event_handler = 'cancel_finished'
		btn.action = raise_event
		self.add_subview(btn)
		
		prev = btn
		# Ok button
		btn = ui.Button(name = 'ok')	
		btn.title = 'OK'
		btn.frame = prev.frame
		btn.event_handler = 'ok_finished'
		btn.action = raise_event
		self.add_subview(btn)
	
		
	def layout(self):
		sv = self.superview
		if not sv: return
		
		self.width = sv.bounds.width
		
		btn = self['today']
		btn.center = self.bounds.center()
		btn.x = 10
		
		btn = self['ok']
		btn.center = self.bounds.center()
		btn.x = self.width - 10 - btn.width
		
		prev = btn
		btn = self['cancel']
		btn.center = self.bounds.center()
		btn.x = prev.frame.min_x - btn.width - 10 
		
		
		
class CalenderDays(ui.View):
	_rows = 5
	_cols = 7
	def __init__(self, dt = None ,  *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.day_btn_list = []
		self.selected_date = None
		self.sel_obj = None
		self.date_selection_color  = get_css_color('orange', .5)
		self.curr_date = dt
		if not self.curr_date:
			self.curr_date = datetime.today()
	
		self.make_view()
		self.goto_year_month(self.curr_date.year, self.curr_date.month)
		
	def make_view(self):
		# create the buttons, add them to the list 'day_btn_list'
		for i in range(self._rows * self._cols):
			btn = make_cal_button(i,  self.cal_select_action)
			self.day_btn_list.append(btn)
			self.add_subview(btn)
			
	def layout(self):
		idx = 0
		r = ui.Rect(*self.bounds)
		w = r.width / self._cols
		h = r.height / self._rows
		
		for i in range(self._rows):
			for j in range(self._cols):
				btn = self.day_btn_list[idx]
				f = ui.Rect(j*w, (i*h), w, h)
				btn.frame = f
				btn.day_lb.frame = btn.bounds.inset(10, 10)
				btn.day_lb.corner_radius = btn.width / 2
				idx += 1
				
	def goto_year_month(self, year, month):
		if self.sel_obj:
			self.sel_obj.day_lb.bg_color = self.sel_obj.bg_color
		dates = get_dates_for_month(year, month)
		
		for i, btn in enumerate(self.day_btn_list):
			d = dates[i]
			btn.date = d
			btn.day_lb.text = str(d.day)
			
			# see if date is same year and month, if not its a day from
			# the past or following month
			if d.year == year and d.month == month:
				btn.alpha = 1
				btn.enabled = True
			else:
				btn.alpha = .3
				btn.enabled = False
				
			today = datetime.today()
			if (d.year, d.month, d.day ) == (today.year, today.month, today.day):
				print('todays date', d)
				
			self.curr_date = datetime(year, month, 1)
			self.set_needs_display()
				
	def cal_select_action(self, sender = None):
		btn = self.day_btn_list[sender.idx]
		self.selected_date = btn.date
		self.sel_obj = sender
		self.set_needs_display()
		raise_event(self, 'date_selected', date = btn.date)
		
	def draw(self):
		'''
			draw a treatment for a  selected date
		'''
		if not self.sel_obj:
			return
			
		btn =self.sel_obj
		# only execute the code below, if the selected date is the
		# same year and monthb
		if self.selected_date:
			if btn.date.year != self.selected_date.year or\
					btn.date.month != self.selected_date.month:
				return
		
		r = ui.Rect(*btn.day_lb.bounds).inset(0,0)
		
		if r.width < r.height:
			r.height = r.width
		else:
			r.width = r.height
			
		r.center(btn.center)
		s = ui.Path.oval(*r)
		ui.set_color(self.date_selection_color)
		s.fill()
		
	@property
	def date(self):
		return self.selected_date
	
		
class IJCalendar(ui.View):
	def __init__(self, date = None,
				first_day_week = calendar.SUNDAY,
				*args, **kwargs):
		super().__init__(*args, **kwargs)
		
		calendar.setfirstweekday(first_day_week)
		self.curr_date = date
		self.sel_obj = None
		
		# if no date passed, we use todays date
		if not self.curr_date:
			self.curr_date = datetime.today()
			
		self.data_model = ModelCalender(date, first_day_week = first_day_week)
		# all the subviews for this view
		self.cv = None
		self.title_bar = None
		self.cal_view = None
		self.days_header = None
		self.tool_bar = None
		
		self.make_view()
		print(self.curr_date)
		self.goto_date(self.curr_date)
	
		
	def make_view(self):
		'''
			Create the views
		'''
		# create a content view,  (Root view) all over views are a 
		# subview if this view
		cv = ui.View(frame = self.bounds, name = '_cv')
		cv.flex = 'WH'
		self.cv = cv 
		self.add_subview(cv)
		
		# Create the title_bar view
		self.title_bar = TitleBar()
		self.cv.add_subview(self.title_bar)
		
		# Create the days header view
		self.days_header = DaysHeader()
		self.cv.add_subview(self.days_header)
		
		# Create the toolbar view
		self.tool_bar = ToolBar()
		self.cv.add_subview(self.tool_bar)
		
		# create the cal_view... 
		self.cal_view = CalenderDays(self.curr_date)
		self.cv.add_subview(self.cal_view)
				
	def layout(self):
		print('in layout cal view')
		y = 0
		if not self.title_bar.hidden:
			self.title_bar.y = y
			y += self.title_bar.height
		
		if not self.days_header.hidden:
			self.days_header.y = y
			y += self.days_header.height
		
		self.cal_view.y = y
		self.cal_view.frame = (0, y, self.cv.width, self.cv.height - y - self.tool_bar.height)
		
		self.tool_bar.y = self.cv.bounds.max_y - self.tool_bar.height
		
	def stylise_day_label(self, **kwargs):
		# not very efficent, but you dont expect that many kwargs
		for btn in self.day_btn_list:
			lb = btn.day_lb
			for k, v in kwargs.items():
				if hasattr(lb, k):
					setattr(lb, k, v)
		
		self.set_needs_display()
		
	@property
	def week_header(self):
		# return the days_header object, so can do -
		# cls.week_header.bg_color = 'red'
		return self.days_header
		
	@property
	def week_header_items(self):
		# returns a generator for the labels used to show the days of 
		# the week
		return (sv for sv in self.days_header.subviews)
	
	
	def goto_year_month(self, year, month):
		self.cal_view.goto_year_month(year, month)
		#self.curr_date = datetime.date(year, month, 1)
		if self.title_bar:
			if hasattr(self.title_bar, 'set_date_title'):
				self.title_bar.set_date_title(datetime(year, month, 1))
				
	
		
	def goto_date(self, dt):
		self.goto_year_month(dt.year, dt.month)
	
	
	def will_close(self):
		print('will_close method')
		
	# called by raise_event, another view communicating with this view
	def goto_next_month(self, sender = None):
		cdate = self.curr_date
		dt = datetime(cdate.year, cdate.month, calendar.monthrange(cdate.year, cdate.month)[1]) + timedelta(days = 1)
		
		self.goto_year_month(dt.year, dt.month)
		self.curr_date = dt
	
		
	def goto_prev_month(self, sender=None):
		cdate = self.curr_date
		dt = datetime(cdate.year, cdate.month, 1) - timedelta(days = 1)
		
		self.goto_year_month(dt.year, dt.month)
		self.curr_date = dt
		
	def goto_today(self, sender=None):
		self.goto_date(datetime.today())
		
	def date_selected(self, sender , **kwargs):
		print(kwargs.get('date', None))

	def cancel_finished(self, sender = None):
		self.cal_view.selected_date = None
		self.close()
		
	def ok_finished(self, sender = None):
		self.close()
		
	def week_header_data_get(self, sender = None):
		return self.data_model.weekday_header()
		
	
	
	@property
	def date(self):
		return self.cal_view.date
	
	@property
	def title_label(self):
		if self.title_bar:
			if hasattr(self.title_bar, 'title_label'):
				return self.title_bar.title_label
		
		return None
	
	# View pass though properties
	@property
	def title_view(self):
		return self.title_bar
	
	@property 
	def day_header_view(self):
		return self.day_header_view
		
							
def date_picker(w, h, date = None,
					first_day_week = calendar.SUNDAY, style ='sheet', 
					animated = False, theme = None , modal = True): 
	frame =(0, 0, w, h)
	cal = IJCalendar(frame = f, name = 'Select a date' , date = date, 
	first_day_week = first_day_week)
	
	editor.present_themed(cal, theme_name=theme,
					style = style, animated=animated,
					hide_title_bar = True)
	if modal:
		cal.wait_modal()
		return cal.date
	print('date_picker complete')


if __name__ == '__main__':
	w, h = 500, 500-36-44
	w, h = 400, 400 		# aspect ratio
	aspect_scale = 1
	w *= aspect_scale
	h *= aspect_scale
	f = (0, 0, w, h)
	style = 'sheet'
	theme = 'Solarized Dark'
	first_day = calendar.SUNDAY
	
	d = datetime(2016, 9 , 1)
	d = None
	x = date_picker(w, h, theme = theme, style =style,
				date =d, first_day_week = first_day)
	#cal_data = ModelCalender()
	print(x)
	_themes = ['Dawn', 'Tomorrow', 'Solarized Light',
	'Solarized Dark', 'Cool Glow', 'Gold', 'Tomorrow Night', 'Oceanic',
	'Editorial']
	
