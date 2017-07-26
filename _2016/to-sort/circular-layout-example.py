# https://forum.omz-software.com/topic/3462/lab-easy-way-to-make-pics-using-ui-button/2

import ui, editor
import calendar
from math import pi

def make_btn(text, w = 256, v=None):
	btn = ui.Button( title = text)
	btn.frame = (0, 0, w, w)
	btn.bg_color = 'teal'
	btn.tint_color = 'white'
	btn.font = ('Arial Rounded MT Bold', w * .4)
	btn.corner_radius = btn.width / 2
	btn.center=v.bounds.center()
	btn.transform=ui.Transform.rotation(-2.*pi*i/N).concat(
	ui.Transform.translation(0,-(v.height/2-btn.height/2))).concat(
	ui.Transform.rotation(2.*pi*i/N))
	return btn
	
w1= 576
v=ui.View(frame=(0,0,w1, w1))
v.bg_color=(1,1,1)
N=12
for i in range(0,N):
	a = make_btn(calendar.month_abbr[i+1], w=48, v=v)
	v.add_subview(a)
	
with ui.ImageContext(w1, w1) as ctx:
	v.draw_snapshot()
	img = ctx.get_image()
	
img.show()

