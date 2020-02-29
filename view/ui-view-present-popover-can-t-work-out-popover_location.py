# coding: utf-8

# https://forum.omz-software.com/topic/2778/ui-view-present-popover-can-t-work-out-popover_location

from __future__ import print_function
import ui

def btn_action(sender):
	print(sender)
	f = (0,0,400, 800)
	pt = tuple(sender.center)
	
	v = ui.View(frame = f)
	loc = ui.convert_point(pt, sender, None)
	#loc = ui.convert_point(loc, None, v)
	v.present('popover', popover_location = tuple(loc) )
	
	
if __name__ == '__main__':
	f = (0,0,500,500)
	v = ui.View(frame = f)
	btn = ui.Button(frame = (100,100, 100, 32))
	btn.border_width = .5
	btn.action = btn_action
	btn.title = 'hello'
	v.add_subview(btn)
	v.present('sheet')

