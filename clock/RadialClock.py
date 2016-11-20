# http://pastebin.com/M165BTzE

from scene import *
from datetime import datetime
from math import sin, cos, radians

WDAYS = ['MON','TUE','WED','THU','FRI','SAT','SUN']

font_HNT = 'HelveticaNeue-Thin'
font_ARB = 'ArialRoundedMTBold'

# scene's text() shorcut
def txt(x,y,t,f=font_HNT,s=14):
	text(t,f,s,x,y)
	
# scene's ellipse() shortcut
def circle(cx,cy,d):
	ellipse(cx-d/2,cy-d/2,d,d)
	
# radius by angle in degree clockwise
def rad(cx,cy,a,r):
	x = cx + r*sin(radians(a))
	y = cy + r*cos(radians(a))
	return x,y
	
# arc by angle in degree clockwise
def arc(cx,cy,a,b,r,t=2,p=0.5):
	i = a
	if a == b: b = b + p # avoid 0
	while i < b:
		x,y = rad(cx,cy,i,r)
		circle(x,y,t) # "stroke" of the arc
		i = i + p # precision in degree
		
def days_of_month(month,year):
	if month == 2:
		# kabisat year
		if (year % 4 == 0) or (year % 1000 == 0):
			result = 29
		else:
			result = 28
	elif month in [1,3,5,7,8,10,12]:
		result = 31
	else: # in [4,6,9,11]
		result = 30
	return result
	
class clock(Scene):
	def setup(self):
		# settings
		self.quartz = False
		self.draw_reff = True
		self.draw_text = True
		self.draw_time = True
		self.draw_date = True
		
	def should_rotate(self, orientation):
		return True # support rotation
		
	def draw(self):
		# get current datetime
		n  = datetime.now()
		wd = datetime.date(n).weekday()
		
		# setup clock dimension
		sz = 12 # arc circle size
		s = sz + 5 # space between arc
		w = self.size.w
		h = self.size.h
		x = w/2 # origin of the clock
		y = h/2
		ls = w > h # landscape
		d = h-s*2 if ls else w-s*2
		r = d/2
		td = '%02d-%02d-%02d'
		tt = '%s, %02d:%02d:%02d'
		
		# setup clock values
		if not self.quartz:
			# milisecond
			msec = n.microsecond / 10000.0
			sec  = (n.second + msec/100) * 6.0
		else:
			sec  = n.second * 6.0
		min  = (n.minute + (1.0*n.second)/60) * 6.0
		pm   = n.hour >= 12; am = not pm
		hour = n.hour-12 if pm else n.hour
		hour = (hour + (1.0*n.minute)/60) * 30.0
		dom  = days_of_month(n.month,n.year)
		wday = (wd + (1.0*n.hour)/24) * 51.5
		day  = (n.day-1 + (1.0*n.hour)/24) * 12
		mon  = (n.month + (1.0*n.day)/dom) * dom
		year = (n.year-2000 + (1.0*n.month)/12) * 3.6
		
		# default style
		background(0.2,0.2,0.2)
		stroke_weight(0)
		stroke(1,1,1,1)
		fill(1,1,1,1)
		
		# draw clock ticks
		if self.draw_reff:
			if not ls:
				arc(x,y,0,360,r,1,6)
				arc(x,y,0,360,r,3,30)
				circle(x,y,2)
				
		# draw clock text
		if self.draw_text:
			txt(x,y+1.2*r+s,'RADIAL CLOCK',font_ARB,22)
			td = td % (n.day,n.month,n.year)
			txt(x,y-1.1*r-s,td)
			tt = tt % (WDAYS[wd],n.hour,n.minute,n.second)
			txt(x,y-1.1*r-2*s,tt)
			
		# draw time arcs
		if self.draw_time:
			fill(1.0,0.0,0.0)
			arc(x,y,0,sec,r-s,sz)
			fill(1.0,0.5,0.0)
			arc(x,y,0,min,r-2*s,sz)
			fill(1.0,1.0,0.0)
			arc(x,y,0,hour,r-3*s,sz)
			fill(0.2,0.2,0.2,1)
			arc(x,y,sec,sec,r-s,sz/2)
			arc(x,y,min,min,r-2*s,sz/2)
			arc(x,y,hour,hour,r-3*s,sz/2)
			
		# draw date arcs
		if self.draw_date:
			fill(0.0,1.0,0.0)
			arc(x,y,0,wday,r-4*s,sz)
			fill(0.0,0.0,1.0)
			arc(x,y,0,day,r-5*s,sz)
			fill(0.5,0.0,0.7)
			arc(x,y,0,mon,r-6*s,sz)
			fill(0.7,0.0,1.0)
			arc(x,y,0,year,r-7*s,sz)
			fill(0.2,0.2,0.2,1)
			arc(x,y,wday,wday,r-4*s,sz/2)
			arc(x,y,day,day,r-5*s,sz/2)
			arc(x,y,mon,mon,r-6*s,sz/2)
			arc(x,y,year,year,r-7*s,sz/2)
			
run(clock())

