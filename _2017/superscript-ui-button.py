# https://forum.omz-software.com/topic/4223/superscript-text-in-ui-button/3

import ui
from objc_util import *


class MyView(ui.View):
	def did_load(self):
		x_pow_y_button = self['x_pow_y_button']
		
		NSMutableAttributedString = ObjCClass('NSMutableAttributedString')
		attributed_string = NSMutableAttributedString.alloc().initWithString_(ns('x2'))
		range = NSRange(1, 1)
		
		attributed_string.superscriptRange(range)
		
		x_pow_y_button_objc = ObjCInstance(x_pow_y_button)
		UIButton = ObjCClass('UIButton')
		for subview in x_pow_y_button_objc.subviews():
			if subview.isKindOfClass(UIButton):
				subview.setAttributedTitle_forState_(attributed_string, 0)
				
				
v = ui.load_view()
v.present('sheet')

