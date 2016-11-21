# https://forum.omz-software.com/topic/3609/gui-textfield-example

import ui

class MyTextFieldDelegate (object):
	def textfield_should_begin_editing(self, textfield):
		return True
	def textfield_did_begin_editing(self, textfield):
		pass
	def textfield_did_end_editing(self, textfield):
		pass
	def textfield_should_return(self, textfield):
		textfield.end_editing()
		return True
	def textfield_should_change(self, textfield, range, replacement):
		return True
	def textfield_did_change(self, textfield):
		print(textfield.text) #only changed this
		#pass
		
f = (0, 0, 300, 480)
v = ui.View(frame=f)
tf = ui.TextField(frame = v.bounds)
tf.height =32
tf.delegate = MyTextFieldDelegate()
v.add_subview(tf)
v.present('sheet')

