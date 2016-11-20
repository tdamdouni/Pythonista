# coding: utf-8

# https://forum.omz-software.com/topic/2879/navigationview-with-constant-background

import ui
v=ui.ImageView(frame=(0,0,576,576))
v.image=ui.Image.named('test:Ruler')

v2=ui.ImageView(frame=v.bounds)
v2.image=ui.Image.named('test:Mandrill')
n=ui.NavigationView(v2)
n.frame=v.bounds

v3=ui.ImageView(frame=v.bounds)
v3.image=ui.Image.named('test:Lenna')

v2.alpha=0.5
v3.alpha=0.5
n.push_view(v3)
v.add_subview(n)
v.present('sheet')

