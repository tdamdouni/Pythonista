# https://forum.omz-software.com/topic/3402/share-position-a-ui-control-in-a-view/6

import ui

def _make_button(title):
	btn = ui.Button()
	btn.width = 80
	btn.height = 32
	btn.border_width = .5
	btn.title = title
	return btn
	
def do_position(obj, pos_code='', pad = 0):
	if not obj.superview:
		return (False, ui.Rect())
		
	# we only reference superview.bounds. hopefully this is correct!
	r = ui.Rect(*obj.superview.bounds)
	
	#obj.center = r.center()
	if 'c' in pos_code:
		pos_code = 'c' + pos_code.replace('c', '')
		
	pos_code = (pos_code or '').lower()
	for i in range(len(pos_code)):
		code = pos_code[i]
		if code is 'c':
			obj.center = r.center()
		elif code is 'l':
			obj.x = r.min_x + pad
		elif code is 'r':
			obj.x = r.max_x - (obj.width+pad)
		elif code is 't':
			obj.y = r.min_y + pad
		elif code is 'b':
			obj.y = r.max_y - (obj.height + pad)
		elif code is 'm':
			obj.y = (r.height / 2) - (obj.height / 2)
			
	return (True, ui.Rect(*obj.frame))
	
	
hide_title_bar = False
style = ''
w = 800
h = 600
f = (0, 0, w, h)
pos_list=['tl', 'tc', 'tr', 'ml', 'mc', 'rm', 'bl', 'bc', 'br' ]
v = ui.View(frame = f, bg_color = 'lightyellow')
v.present(style = style, hide_title_bar = hide_title_bar )

for pos_code in pos_list:
	btn = _make_button(pos_code)
	v.add_subview(btn)
	# do_position, can only be called after its been added to a view.
	# does need to be like this, but it makes sense to do it this way.
	do_position(btn, pos_code, 30)
	
# ----------------

def do_position(obj, pos_code='', pad=0):
	if not obj.superview:
		return (False, ui.Rect())
		
	# we only reference superview.bounds. hopefully this is correct!
	r = obj.superview.bounds
	obj.center = r.center()
	
	pos_code = (pos_code or '').lower()
	if 'l' in pos_code:
		obj.x = r.min_x + pad
	elif 'r' in pos_code:
		obj.x = r.max_x - (obj.width+pad)
	if 't' in pos_code:
		obj.y = r.min_y + pad
	elif 'b' in pos_code:
		obj.y = r.max_y - (obj.height + pad)
		
	return (True, obj.frame)

