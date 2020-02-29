from __future__ import print_function
# https://forum.omz-software.com/topic/3175/how-to-trigger-an-action-when-a-textfield-is-edited

import ui

class MyTextFieldDelegate(object):
	def textfield_did_change(self, textfield):
		print(textfield.text)
		
textfield = ui.TextField()
textfield.delegate = MyTextFieldDelegate()

# --------------------

def myfun(sender):
	print(sender.text)
	
v=ui.load_view(your_pyui_name)

# --------------------

v=ui.load_view(your_pyui_name)
v['textfield1'].action=myfun

# --------------------

