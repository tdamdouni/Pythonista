#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2724/spacing-of-buttonitem-s/6

# https://gist.github.com/marcus67/9804a9f1c727b76f2364

from __future__ import print_function
import ui
from objc_util import *

v = ui.View(frame=(0, 0, 400, 400), name='Demo')
v.background_color = 'white'

btn_images = [ui.Image.named(n) for n in ['iob:beaker_32', 'iob:beer_32', 'iob:coffee_32']]
btn_container = ui.View(frame=(0, 0, len(btn_images)*32, 44))
for i, img in enumerate(btn_images):
	btn = ui.Button(image=img)
	btn.frame = (i*32, 0, 32, 44)
	btn_container.add_subview(btn)
	
btn_item = ui.ButtonItem()
btn_item_objc = ObjCInstance(btn_item)
btn_item_objc.customView = ObjCInstance(btn_container)
v.right_button_items = [btn_item]
v.present('sheet')

#==============================

# coding: utf-8
# This file is part of https://github.com/marcus67/rechtschreibung

import ui
from objc_util import *

DEFAULT_X_SPACING = 8
DEFAULT_HEIGHT = 44

class ButtonItemCondenser (object):

	def __init__(self, button_item_list, x_spacing=DEFAULT_X_SPACING):
	
		self.button_item_list = button_item_list
		self.x_spacing = x_spacing
		
	def get_condensed_list(self):
	
		# see https://forum.omz-software.com/topic/2724/spacing-of-buttonitem-s
		i = 0
		x = 0
		btn_container = ui.View(name='test')
		
		for button_item in self.button_item_list:
			btn = ui.Button(image=button_item.image, action=button_item.action)
			#button_item.action(btn_container)
			width = button_item.image.size[0]
			btn.frame = (x, 0, width, DEFAULT_HEIGHT)
			x = x + width + self.x_spacing
			btn_container.add_subview(btn)
			i = i + 1
			
		x = x - self.x_spacing
		btn_container.frame = (0, 0, x , DEFAULT_HEIGHT)
		btn_item = ui.ButtonItem()
		btn_item_objc = ObjCInstance(btn_item)
		btn_item_objc.customView = ObjCInstance(btn_container)
		return [btn_item]
		
def handle_action(sender):
	#print "handle_action: sender.name=%s" % sender.name
	print(str(sender))
	
#def handle_action():
#  print "handle_action"

def test():

	icon_names = [ 'iob:beaker_32', 'iob:beer_32', 'iob:bag_32' ]
	
	button_item_list = map(lambda name : ui.ButtonItem(image=ui.Image.named(name), action=handle_action), icon_names)
	condenser = ButtonItemCondenser(button_item_list)
	
	v = ui.View(frame=(0, 0, 400, 400), name='Demo')
	v.background_color = 'white'
	condensed_list = condenser.get_condensed_list()
	normal_item = ui.ButtonItem(image=ui.Image.named('iob:checkmark_32'), action=handle_action)
	condensed_list.append(normal_item)
	v.right_button_items = condensed_list
	v.present('sheet')
	
if __name__ == '__main__':
	test()

