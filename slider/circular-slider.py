# https://forum.omz-software.com/topic/3449/share-a-list-of-rects-distributed-around-360-degrees/32

import ui
from math import pi,atan2

class CircularSlider(ui.View):
	def __init__(self,*args,**kwargs):
		ui.View.__init__(self,*args,**kwargs)
		self.a = 0
		self.value = (self.a+pi)/(2*pi)
		
	def draw(self):
		scl=min(self.width,self.height)
		self.scl=scl
		btn_siz=min(22/scl,0.05)
		#work in normalized units
		ui.concat_ctm(ui.Transform.scale(scl,scl))
		#origin at center
		ui.concat_ctm(ui.Transform.translation(.5,.5))
		ui.set_color('#1aa1b5')
		o = ui.Path.oval(-.5+btn_siz, -.5+btn_siz, 1-2*btn_siz, 1-2*btn_siz)
		o.line_width=2/scl
		o.stroke()
		#rotate by angle
		ui.concat_ctm(ui.Transform.rotation(self.a))
		# center origin at button
		ui.concat_ctm(ui.Transform.translation(.5-btn_siz,0))
		#optional: to keep images upright
		#ui.concat_ctm(ui.Transform.rotation(-self.a))
		p=ui.Path.oval(-btn_siz,-btn_siz,2*btn_siz,2*btn_siz)
		p.fill()
		
	def touch_moved(self,touch):
		dp=touch.location-touch.prev_location
		self.a=atan2(touch.location.y-self.scl/2.,touch.location.x-self.scl/2.)
		self.value = (self.a+pi)/(2*pi)
		self.set_needs_display()
		
	def touch_ended(self, touch):
		print(self.value)
		
d = CircularSlider(frame=(0,0,500, 500),bg_color='white')
d.present('sheet')

