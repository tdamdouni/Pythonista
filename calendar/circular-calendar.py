# https://forum.omz-software.com/topic/3449/share-a-list-of-rects-distributed-around-360-degrees/28

import ui, calendar
from math import pi, sin, radians

def make_button(i, v, N):
	def button_action(sender):
		print('Button {} was pressed.'.format(sender.title))
		
	btn = ui.Button(title=calendar.month_abbr[i+1])
	btn.action = button_action
	btn.height=btn.width=64
	btn.alpha = sin(radians(15.+75.0/(N-1)*i))
	btn.border_width = .5
	btn.corner_radius = btn.width *.5
	btn.bg_color = 'orange'
	btn.text_color = btn.tint_color = 'black'
	center_x, center_y = v.bounds.center()
	btn.center = (btn.width/2+5.0, center_y) #v.bounds.center()
	btn.transform=ui.Transform.translation(0,-(v.height/2-btn.height/2)
	).concat(ui.Transform.rotation(2.*pi*i/N))
	return btn
	
v=ui.View(frame=(0,0,576,576))
v.bg_color=(1,1,1)
N = 12
N1 = 7
for i in range(0,N1):
	v.add_subview(make_button(i, v, N))
v.present('sheet')

