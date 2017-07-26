# https://gist.github.com/jsbain/84489b13a17cdd46288f16b50b2f7bc3

import ui
from math import pi,atan2
class Drag(ui.View):
	def __init__(self,*args,**kwargs):
		ui.View.__init__(self,*args,**kwargs)
		self.a=.3
	def draw(self):
		scl=min(self.width,self.height)
		self.scl=scl
		btn_siz=min(22/scl,0.05)

		#work in normalized units
		ui.concat_ctm(ui.Transform.scale(scl,scl))
		#origin at center
		ui.concat_ctm(ui.Transform.translation(.5,.5))
		#rotate by angle
		ui.concat_ctm(ui.Transform.rotation(self.a))
		#stroke line from center to edge
		ui.set_color('#1aa1b5')
		l=ui.Path()
		l.move_to(.0,0)
		l.line_to(.5-btn_siz,0)			
		l.line_width=2/scl
		l.stroke()
		# center origin at button
		ui.concat_ctm(ui.Transform.translation(.5-btn_siz,0))
		#optional: to keep images upright
		#ui.concat_ctm(ui.Transform.rotation(-self.a))
		p=ui.Path.oval(-btn_siz,-btn_siz,2*btn_siz,2*btn_siz)
		p.fill()

	def touch_moved(self,touch):
		dp=touch.location-touch.prev_location
		self.a=atan2(touch.location.y-self.scl/2.,touch.location.x-self.scl/2.)
		self.set_needs_display()
			
d=Drag(frame=(0,0,500,500),bg_color='white')
d.present('sheet')
