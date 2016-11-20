# https://forum.omz-software.com/topic/3402/share-position-a-ui-control-in-a-view

# Phuket2 , Pythonista Forums (Python profiency, not much)
# works for python 2 or 3
import ui

def _make_button(title):
	btn = ui.Button()
	btn.width = 80
	btn.height = 32
	btn.border_width = .5
	btn.title = title
	return btn
	
def do_position(obj, pos_code='', pad = 0):
	'''
	do_position:
	a very simple positioning function for ui elements. as simple
	as it is can be useful. especially for testing.
	
	args:
	1. obj - a ui object Instance such as a ui.Button
	
	2. pos_code - 1 to x letters or combinations in the set
	('c', 't', 'l','b', 'r'). eg 'c' will postion the obj in
	the middle of the parent view. 'tc' or 'ct' will position
	the obj at the top center if the screen.
	
	3. pad - is to give a type of margin from the edges.
	for t and l pad is added, for b and r pad is subtracted.
	c is not effected by pad
	
	returns: a tuple (boolean, ui.Rect)
	if False, exited early, eg, not yet added to a view.
	ui.Rect will be set as (0, 0, 0, 0)
	if True, the ui.Rect is set to the frame of the object.
	regardless if it moved or not.
	if both cases ui.Rect will be a valid ui.Rect
	'''
	
	# if the control is not added to a view, i.e no superview, we cant
	# do much other than return
	if not obj.superview:
		return (False, ui.Rect())
		
	# we only reference superview.bounds. hopefully this is correct!
	r = ui.Rect(*obj.superview.bounds)
	
	# in the func we only deal with lowercase pos_code. we normalise
	# the case so upper or lower or a mixture can be used as input
	pos_code = pos_code.lower()
	
	# c for center is a special case. does not know if you want vertical
	# or horizontal center. we delete c from input if it exists and
	# make sure its the first operation. then we dont get side effects
	if 'c' in pos_code:
		pos_code = 'c' + pos_code.replace('c', '')
		
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
		elif code is 'r':
			obj.y = r.max_y - (obj.height + pad)
			
	return (True, ui.Rect(*obj.frame))
	
	
hide_title_bar = False
style = ''

w = 800
h = 600

f = (0, 0, w, h)
pos_list=['c','tl','tc','tr','lc', 'cr', 'bl', 'bc', 'br']
v = ui.View(frame = f, bg_color = 'lightyellow')
v.present(style = style, hide_title_bar = hide_title_bar )

for pos_code in pos_list:
	btn = _make_button(pos_code)
	v.add_subview(btn)
	# do_position, can only be called after its been added to a view.
	# does need to be like this, but it makes sense to do it this way.
	do_position(btn, pos_code, 30)
# --------------------

