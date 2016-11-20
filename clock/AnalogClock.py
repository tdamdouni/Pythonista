# http://pastebin.com/pCUuWfSW

from scene import *
from datetime import datetime
from math import sin, cos, radians

font = 'HelveticaNeue-Thin'

# scene's text() shorcut
def txt(x,y,t,f=font,s=14):
	text(t,f,s,x,y)
	
# scene's ellipse() shortcut
def circle(cx,cy,d,t=2):
	stroke_weight(t)
	ellipse(cx-d/2,cy-d/2,d,d)
	
# radius by angle in degree clockwise
def rad(cx,cy,a,r):
	x = cx + r*sin(radians(a))
	y = cy + r*cos(radians(a))
	return x,y
	
class clock(Scene):
	def setup(self):
		# settings
		self.quartz = False
		
	def should_rotate(self, orientation):
		return True # support rotation
		
	def draw(self):
		# get current datetime
		n = datetime.now()
		
		# setup clock dimension
		sz = 14 # arc circle size
		s = sz + sz/2 # space between arc
		w = self.size.w - 2*sz # offset
		h = self.size.h - 2*sz
		x = w/2 + sz # origin of the clock
		y = h/2 + sz
		d = h-s*2 if w > h else w-s*2
		r = d/2
		t = '%02d:%02d:%02d'
		
		# setup clock values
		if not self.quartz:
			# milisecond
			msec = n.microsecond / 10000.0
			sec  = (n.second + msec/100) * 6.0
		else:
			sec  = n.second * 6.0
		min  = (n.minute + (1.0*n.second)/60) * 6.0
		hour = n.hour-12 if n.hour > 12 else n.hour
		hour = (hour + (1.0*n.minute)/60) * 30.0
		
		# default style
		background(0.2,0.2,0.2)
		stroke(1,1,1,1)
		fill(0,0,0,0)
		
		# draw clock ticks
		for i in range(0,360,6):
			ax,ay = rad(x,y,i,r)
			circle(ax,ay,1)
		for i in range(0,360,30):
			ax,ay = rad(x,y,i,r)
			circle(ax,ay,4)
			
		# draw clock text
		txt(x,y+1.25*r+s,'ANALOG CLOCK')
		t = t % (n.hour,n.minute,n.second)
		txt(x,y-1.2*r-s,t)
		for i in range(0,360,30):
			ax,ay = rad(x,y,i,r-s)
			if i == 0: i = 360 # avoid 0
			txt(ax,ay,str(i/30))
			
		# draw second hand
		ax,ay = rad(x,y,sec,r)
		circle(ax,ay,sz,2)
		ax,ay = rad(x,y,sec,r-sz/2)
		line(x,y,ax,ay)
		ax,ay = rad(x,y,sec-180,s) # tail
		line(x,y,ax,ay)
		
		# draw minute hand
		ax,ay = rad(x,y,min,r-s)
		circle(ax,ay,1.5*sz,4)
		ax,ay = rad(x,y,min,r-s-sz/2)
		line(x,y,ax,ay)
		ax1,ay1 = rad(x,y,min,r-s+sz/2)
		ax2,ay2 = rad(x,y,min,r-s+sz/2+sz)
		line(ax1,ay1,ax2,ay2) # pointer
		
		# draw hour hand
		ax,ay = rad(x,y,hour,r/2.5)
		circle(ax,ay,2*sz,8)
		ax,ay = rad(x,y,hour,r/2.5-sz/2)
		line(x,y,ax,ay)
		ax1,ay1 = rad(x,y,hour,r/2.5-sz/2+sz)
		ax2,ay2 = rad(x,y,hour,r/2.5-sz/2+2*sz)
		line(ax1,ay1,ax2,ay2) # pointer
		
		# draw center
		fill(.2,.2,.2,1)
		circle(x,y,1.5*sz)
		
run(clock())

