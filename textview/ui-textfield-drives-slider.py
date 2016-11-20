# coding: utf-8

# https://forum.omz-software.com/topic/3051/ui-textfield-drives-slider/5

import ui

def slider_action(sender):
	# get the sliders superview a.k.a view
	v = sender.superview
	v['mylabel'].text = str(sender.value)
	
if __name__ == '__main__':
	f = (0, 0, 300, 400)
	v = ui.View(frame = f, bg_color = 'white')
	slider = ui.Slider()
	slider.action = slider_action
	slider.width= v.width
	lb = ui.Label(name = 'mylabel')
	lb.text = '0'
	lb.y = slider.y + 20
	
	v.add_subview(slider)
	v.add_subview(lb)
	v.present('sheet')
	
# --------------------

# coding: utf-8

import ui
import string

class MyTextFieldDelegate (object):
	def textfield_should_begin_editing(self, textfield):
		return True
	def textfield_did_begin_editing(self, textfield):
		pass
	def textfield_did_end_editing(self, textfield):
		pass
	def textfield_should_return(self, textfield):
		textfield.end_editing()
		self.update_slider(textfield)
		return True
	def textfield_should_change(self, textfield, range, replacement):
		if not range:
			self.update_slider(textfield)
			return True
			
		if replacement not in string.digits :
			return False
			
		return True
	def textfield_did_change(self, textfield):
		pass
		
	def update_slider(self, textfield):
		val = float(textfield.text) / 100.
		slider = textfield.superview['myslider']
		slider.value  = val
		
		
		
def slider_action(sender):
	# get the sliders superview a.k.a view
	v = sender.superview
	v['mylabel'].text = str(sender.value)
	
if __name__ == '__main__':
	f = (0, 0, 300, 400)
	v = ui.View(frame = f, bg_color = 'white')
	slider = ui.Slider()
	slider.name = 'myslider'
	slider.action = slider_action
	slider.width= v.width
	lb = ui.Label(name = 'mylabel')
	lb.text = '0'
	lb.y = slider.y + 20
	
	tf = ui.TextField()
	tf.height = lb.height
	tf.delegate = MyTextFieldDelegate()
	tf.y = lb.y + lb.height + 20
	tf.text_color = 0
	
	
	
	v.add_subview(slider)
	v.add_subview(lb)
	v.add_subview(tf)
	v.present('sheet')
	
# --------------------

