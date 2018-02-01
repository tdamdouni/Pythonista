# https://forum.omz-software.com/topic/4355/scripter-pythonista-ui-animation-framework-built-on-ui-view-update/23

from scripter import *
import ui
import scene_drawing

@script
def custom_action(my_view):
	move(my_view, 200, 200)
	pulse(my_view, 'red')
	yield 1
	hide(my_view)
	
@script
def custom_reverse_action(my_view):
	show(my_view)
	yield
	move(my_view, 100, 20)
	pulse(my_view, 'black')
	
toggle = True
def button_action(sender):
	global toggle
	
	s = sender.superview
	ease_func = scene_drawing.curve_sinodial
	#ease_func = scene_drawing.curve_ease_in
	#ease_func = scene_drawing.curve_ease_out
	#ease_func = scene_drawing.curve_ease_back_in
	#ease_func = scene_drawing.curve_ease_back_out
	l = s['label1']
	title = sender.title
	if title == 'move':
		if toggle:
			move(l, 200, 200, ease_func=ease_func)
		else:
			move(l, 100,20, ease_func=ease_func)
	elif title == 'hide':
		if toggle:
			hide(l, ease_func=ease_func)
		else:
			show(l, ease_func=ease_func)
	elif title == 'rotate':
		if toggle:
			rotate(l, 30, ease_func=ease_func)
		else:
			rotate(l, 0, ease_func=ease_func)
	elif title == 'custom':
		if toggle:
			custom_action(l)
		else:
			custom_reverse_action(l)
	elif title == 'color':
		if toggle:
			slide_color(l, 'text_color', 'green')
		else:
			slide_color(l, 'text_color', 'black')
	elif title == 'count':
		if toggle:
			set_value(l, 'text', range(1,101),
			lambda c: f'count: {c}')
		else:
			set_value(l, 'text', range(100, 0, -1),
			lambda c: 'Text to be animated' if c == 1 else f'count: {c}')
	elif title == 'fly_out':
		if toggle:
			fly_out(l, 'down')
		else:
			move(l, 100, 20)
	elif title == 'font_sz':
		if toggle:
			slide_value(l, 'font', 40, start_value=20, map_func=lambda sz: ('Helvetica', sz) )
		else:
			slide_value(l, 'font', 20, start_value=40, map_func=lambda sz: ('Helvetica', sz) )
	toggle = not toggle
	
v = ui.View(frame=(0,0,400,400))
l = ui.Label(text='Text to be animated', font=('Helvetica', 20),
            name='label1', frame=(100,20,200,100))
b1 = ui.Button(title='move', frame=(20, 300, 80,50), action=button_action)
b2 = ui.Button(title='hide', frame=(120, 300, 80,50), action=button_action)
b3 = ui.Button(title='rotate', frame=(220, 300, 80,50), action=button_action)
b4 = ui.Button(title='custom', frame=(320, 300, 80,50), action=button_action)
b5 = ui.Button(title='color', frame=(20, 350, 80,50), action=button_action)
b6 = ui.Button(title='count', frame=(120, 350, 80,50), action=button_action)
b7 = ui.Button(title='fly_out', frame=(220, 350, 80,50), action=button_action)
b8 = ui.Button(title='font_sz', frame=(320, 350, 80,50), action=button_action)
v.add_subview(l)
v.add_subview(b1)
v.add_subview(b2)
v.add_subview(b3)
v.add_subview(b4)
v.add_subview(b5)
v.add_subview(b6)
v.add_subview(b7)
v.add_subview(b8)
v.present('sheet')

