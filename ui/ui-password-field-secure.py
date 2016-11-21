# https://forum.omz-software.com/topic/3408/password-fields-in-ui/4

import ui

_font = ('Menlo', 24)
#_font = ('<System>', 24)

def btn_action(sender):
	fld = sender.superview['pwd']
	fld.secure = not fld.secure
	fld.font = _font
	if fld.secure:
		sender.title = 'Clear Text'
	else:
		sender.title = 'Protected'
		
v = ui.View(frame=(0,0,400,100), bg_color ='white')
t = ui.TextField(name = 'pwd', frame=(0,0,v.width, 48))
t.font= _font
#t.secure = True
t.secure = False
v.add_subview(t)
btn = ui.Button(frame = (10,0, 80, 32), title = 'Protected')
btn.y = t.frame.max_y + 10
btn.width += btn.width * 1
btn.border_width = .5
btn.corner_radius = 3
btn.action = btn_action
v.add_subview(btn)
v.present('sheet')

