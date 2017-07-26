# https://gist.github.com/jsbain/6fc02b7d75eb22111b826cfdb2394697

import ui
from math import pi
v=ui.View(frame=(0,0,576,576))
v.bg_color=(1,1,1)
N=12
for i in range(0,N):
	a=ui.Button(image=ui.Image.named('iob:arrow_up_a_256'))
	a.height=a.width=64
	a.center=v.bounds.center()
	a.transform=ui.Transform.translation(0,-(v.height/2-a.height/2)).concat(
		ui.Transform.rotation(2.*pi*i/N))
	v.add_subview(a)
v.present('sheet')
