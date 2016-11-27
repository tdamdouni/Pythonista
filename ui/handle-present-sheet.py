# coding: utf-8

# https://forum.omz-software.com/topic/2544/wish-list-for-next-release/81

import ui

class AnyCustomClass(ui.View):
	def __init__(self, *args , **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
if __name__ == '__main__':
	_factor = .50
	f = (0,0, ui.get_screen_size()[0] * _factor, ui.get_screen_size()[1] * _factor )
	v  = ui.View(frame = f, bg_color = 'green')
	acc = AnyCustomClass(frame = (f))
	v.add_subview(acc)
	v.present('sheet')

