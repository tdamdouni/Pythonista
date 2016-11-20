# coding: utf-8

# https://github.com/sanit/pythonista/blob/master/calview.py

# https://forum.omz-software.com/topic/2953/calendar-view-class

import ui
import datetime as dt

class CalendarView(object):

	def __init__(self,fldname,dateval,action=None):
		self.days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
		self.width,self.height = ui.get_screen_size()
		cv = ui.View(name=fldname)
		cv.frame = (0,95,self.width,255)
		cv.background_color = 'yellow'
		cv.border_color = 'yellow'
		cv.border_width = 2
		self.view = cv
		self.action = action 
		prv_mth = ui.Button(title='<')
		prv_mth.frame = (5,5,50,25)
		prv_mth.action = self.prev_pressed
		self.day_color = prv_mth.tint_color 
		self.view.add_subview(prv_mth)
		nxt_mth = ui.Button(title='>')
		nxt_mth.frame = (56,5,50,25)
		nxt_mth.action = self.next_pressed
		self.view.add_subview(nxt_mth)
		label = ui.Label(name='caltitle')
		self.caldate = dateval #dt.datetime.strptime(dateval,'%d/%m/%Y')
		self.curdate = curdate = dt.datetime.today()
		label.text = str(self.caldate.strftime('%B  %Y'))
		label.frame = (107,5,200,25)
		label.alignment = ui.ALIGN_CENTER
		self.view.add_subview(label)
		today_btn = ui.Button(title='Today')
		today_btn.frame = (self.width-60,5,50,25)
		today_btn.action = self.today_pressed
		self.view.add_subview(today_btn)
		self.firstdate = dt.date(self.caldate.year,self.caldate.month,1)
		self.create_buttons()
		self.draw_calendar()

	def create_buttons(self):
		for i in range(0,49):
			if i<7:
				daytitle = self.days[i]
			else:
				daytitle = ''
			button = ui.Button(name='day'+str(i),title=daytitle)
			if i>=7:
				button.action = self.button_pressed
			button.frame = (5+(i%7)*51,31+(i/7)*31,50,30)
			button.border_color = '#dadada'
			button.border_width = 1
			if i%7 == 0:
				button.background_color = '#fff5f5'
			else:
				button.background_color = 'white'
			self.view.add_subview(button)			

	def draw_calendar(self):
		self.lastdate = self.last_day_of_month(self.firstdate)
		self.firstweekday = self.firstdate.weekday()
		if self.firstweekday==6:
			self.firstweekday = 0 
		else:
			self.firstweekday = self.firstweekday+1
		last_day = self.lastdate.day
		self.view['caltitle'].text = str(self.firstdate.strftime('%B  %Y'))
		for i in range(7,49):
			dy = i-6-self.firstweekday
			if (self.firstweekday+7<=i) and dy<=last_day:
				strtitle = str(dy)
			else:
				strtitle = ''
			self.view['day'+str(i)].title = strtitle
			if (self.firstdate.year == self.curdate.year) and (self.firstdate.month == self.curdate.month) and (self.curdate.day == dy):
				self.view['day'+str(i)].tint_color = 'red'
			elif (self.firstdate.year == self.caldate.year) and (self.firstdate.month == self.caldate.month) and (self.caldate.day == dy):
				self.view['day'+str(i)].tint_color = 'black'
			else:
				self.view['day'+str(i)].tint_color =  self.day_color

	def button_pressed(self,sender):
		self.caldate = dt.date(self.firstdate.year,self.firstdate.month,int(sender.title))
		if not (self.action is None):
			(self.action)(self)

	def prev_pressed(self,sender):
		if self.firstdate.month == 1:
			self.firstdate = dt.date(self.firstdate.year-1,12,1)
		else:
			self.firstdate = dt.date(self.firstdate.year,self.firstdate.month-1,1)
		self.draw_calendar()

	def next_pressed(self,sender):
		if self.firstdate.month == 12:
			self.firstdate = dt.date(self.firstdate.year+1,1,1)
		else:
			self.firstdate = dt.date(self.firstdate.year,self.firstdate.month+1,1)
		self.draw_calendar()

	def today_pressed(self,sender):
		self.firstdate = dt.date(self.curdate.year,self.curdate.month,1)
		self.draw_calendar()

	def last_day_of_month(self,date):
		if date.month == 12:
			return date.replace(day=31)
		return date.replace(month=date.month+1, day=1) - dt.timedelta(days=1)

def calendar_action(sender):
	print(sender.caldate)
	sender.view.close()

if __name__ == '__main__':
	vw = CalendarView('Calendar',dt.datetime.today(),calendar_action)
	vw.view.present('default')
