# https://forum.omz-software.com/topic/3408/password-fields-in-ui

import ui

v = ui.View(frame=(0,0,400,100))
t = ui.TextField(frame=v.frame)
#t.secure = True
t.secure = False
v.add_subview(t)
v.present('sheet')
