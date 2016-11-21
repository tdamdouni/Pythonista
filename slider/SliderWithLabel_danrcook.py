# https://gist.github.com/danrcook/5b35e47628d28daec1d5ec7e909b4f95

'''
SliderWithLabel is a wrapper for ui.Slider() for use in Pythonista on iOS. Provides an editable label for the display and setting of the slider value.

See SliderWithLabel class for detailed usage.
'''

__author__ = '@cook'

import ui

class SliderWithLabel(ui.View):
	'''Wrapper for ui.Slider to also show a label. You can edit the value of the slider directly in the label since it is a textfield.
	Keyword Arguments for SliderWithLabel:
	-action: define a function to receive information when a slider has been slid
	
	SliderWithLabel can be initialized with arguments specific to the slider and label:
	
	Keyword Arguments for the slider:
	- value: default value when presented (should less than max_val and greater than 0). Default is 50
	- max_val: the default for a usual slider is 1.0. SliderWithLabel will conventiently multiply the max_val for the label display and for returning it's value attribute. The default is 100
	- slider_tint_color for the color of the slider bar (up to current point). Default is 0.7 (gray)
	
	Keyword arguments for the label:
	- label_bgcolor: default is 1 (white)
	- label_border_color: default is 0.7 (light gray)
	- label_border_width: default is 0.5
	- label_corner_radius: default is 5
	- label_font: default is ('<system>', 11)
	- label_text_color: default is 0.7
	- label_keyboard_type: default is ui.KEYBOARD_DECIMAL_PAD
	- label_alignment: default is ui.ALIGN_CENTER
	- label_alpha: default is 1
	- label_bordered: default is False (this will override style attributes and just be a white rect with frame)
	
	Other:
	- values are rounded in the label and for SliderWithLabel.value
	- SliderWithLabel needs some vertical space: recommonded height of 60
	- use SliderWithLabel.value for returning a value between 0 and SliderWithLabel.max_val
	'''
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.max_val = kwargs['max_val'] if 'max_val' in kwargs else 100
		self.value = round(kwargs['value']) if 'value' in kwargs else round(self.max_val/2) #for convenience in getting the value attribute
		self.make_view(**kwargs)
		self.action = kwargs['action'] if 'action' in kwargs else None
		
	def make_view(self, **kwargs):
		slider = ui.Slider()
		slider.value = kwargs['value']/self.max_val if 'value' in kwargs else 0.5
		slider.action = self.update_label_and_value
		slider.tint_color = kwargs.get('slider_tint_color', 0.7)
		label = self.make_label(**kwargs)
		self.add_subview(slider)
		self.add_subview(label)
		self.label = label
		self.slider = slider
		
	def make_label(self, **kwargs):
		label = ui.TextField()
		label.action = self.update_value
		label.text = str(self.value)
		label.bordered = False
		defaults = {'background_color': 1,
		'border_color': 0.7,
		'border_width': 0.5,
		'corner_radius': 5,
		'font': ('<system>', 11),
		'text_color': 0.7,
		'keyboard_type': ui.KEYBOARD_DECIMAL_PAD,
		'alignment': ui.ALIGN_CENTER,
		'alpha': 1,
		'bordered': False,
		'frame': (0,0,100,100)}
		for attr in defaults:
			setattr(label, attr, kwargs['label_' + attr]) if 'label_' + attr in kwargs\
			else setattr(label, attr, defaults[attr])
		if label.bordered:
			label.background_color = (0,0,0,0) #because the background will still show on bordered
		return label
		
	def update_value(self, sender):
		try:                    #try/except in case wrong text is entered...
			if 0 < int(self.label.text) < self.max_val:
				self.slider.value = int(self.label.text)/self.max_val
				self.update_label_and_value(self)
			else:
				self.label.text = str(self.value) #if out of slider min/max reset label to previous
		except:
			self.label.text = str(self.value) #essentially do nothing for wrong text, reset to previous
			
	def update_label_and_value(self, sender):
		self.label.x = (self.slider.width - 34) * self.slider.value - (self.label.width/2) + 17
		self.value = round(self.slider.value*self.max_val)
		self.label.text = str(self.value)
		
		#so the label doesn't go off-view:
		if self.label.x + self.label.width > self.width:
			self.label.x = self.width - self.label.width
		if self.label.x < 0:
			self.label.x = 0
			
		#for sending self to action
		if self.action and callable(self.action):
			self.action(self)
			
	def layout(self):
		#some of these constants are just to define the layout for the sake of design
		self.height = 60 if self.height < 60 else self.height #should be 60 or more otherwise clipping will occur
		self.slider.frame = (0,self.height/2-7,self.width, 34)
		self.label.width, self.label.height = 46, 20
		self.label.y = self.slider.y - (self.label.height + 2)
		self.label.x = (self.slider.width - 34) * self.slider.value - (self.label.width/2) + 17
		
if __name__ == '__main__':
	#simple example of three sliders with different names
	#ability to set a function as an action for the SliderWithLabel
	
	view = ui.View()
	
	def get_value(sender):
		view.name = str(sender.value)
		
	w = ui.get_window_size()[0]
	a = SliderWithLabel(name='a', frame=(10,30,w-20,60), value=30, max_val=300, label_background_color='#223322', action=get_value)
	b = SliderWithLabel(name='b', frame=(10,90,w-20,60), value=75, max_val=100, action=get_value)
	c = SliderWithLabel(name='c', frame=(10,150,w-20,60), max_val=1000, label_background_color='#aa0000', label_text_color=1, action=get_value)
	view.add_subview(a)
	view.add_subview(b)
	view.add_subview(c)
	view.background_color = 1
	view.present()

