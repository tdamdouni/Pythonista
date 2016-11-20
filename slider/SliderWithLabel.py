# https://gist.github.com/danrcook/5b35e47628d28daec1d5ec7e909b4f95

# https://forum.omz-software.com/topic/3353/share-code-sliderwithlabel-class-for-ui-slider-featuring-editable-label

'''
SliderWithLabel is a wrapper for ui.Slider() for use in Pythonista on iOS. Provides an editable label for the display and setting of the slider value.

See SliderWithLabel class for detailed usage.
'''

__author__ = '@cook'

import ui

class SliderWithLabel(ui.View):
	'''wrapper for ui.Slider to also show a label. You can edit the value of the slider directly in the label since it is a textfield. Can take the following keyword arguments:
	- for the slider:
	>> value: default value when presented (should be a number that is less than max_val and greater than 0). The default is 50
	>> max_val: the default for a usual slider is 1.0. SliderWithLabel will conventiently multiply the max_val for the label display and for returning it's value attribute. The default is 100
	>> tint_color for the color of the slider bar (up to current point). Default is 0.7 (gray)
	- values are rounded in the label and for SliderWithLabel.value
	- SliderWithLabel needs some vertical space: has a height of 60
	- use SliderWithLabel.value for return a value between 0 and SliderWithLabel.max_val
	
	Delegate: use an object with a method of value_did_change and set SliderWithLabel.delegate'''
	
	def __init__(self, **kwargs):
		self.frame = kwargs['frame'] if 'frame' in kwargs else (0,0,100,60)
		self.slider = ui.Slider()
		self.max_val = kwargs['max_val'] if 'max_val' in kwargs else 100
		self.slider.value = kwargs['value']/self.max_val if 'value' in kwargs else 0.5
		self.value = round(self.slider.value*self.max_val) #for convenience in getting the value attribute
		self.slider.action = self.update_label_and_value
		self.slider.tint_color = kwargs['tint_color'] if 'tint_color' in kwargs else 0.7
		self.label = ui.TextField()
		self.label.action = self.update_value
		self.label.bordered = True
		self.label.alignment = ui.ALIGN_CENTER
		self.label.font = ('<system>',11)
		self.label.text_color = kwargs['text_color'] if 'text_color' in kwargs else 0.7
		self.label.text = str(self.value)
		self.add_subview(self.slider)
		self.add_subview(self.label)
		
	def update_value(self, sender):
		try:                    #try/except in case wrong text is entered...
			self.slider.value = int(self.label.text)/self.max_val
			self.update_label_and_value(self)
		except:
			pass
			
	def update_label_and_value(self, sender):
		self.label.x = (self.slider.width - 34) * self.slider.value - (self.label.width/2) + 17
		self.value = round(self.slider.value*self.max_val)
		self.label.text = str(self.value)
		if self.label.x + self.label.width > self.width:
			self.label.x = self.width - self.label.width
		if self.label.x < 0:
			self.label.x = 0
		#for delegate
		if self.delegate and hasattr(self.delegate, 'slider_value_did_change'):
			if callable(self.delegate.slider_value_did_change):
				self.delegate.slider_value_did_change(self.value)
				
	def draw(self):
		self.height = 60
		self.slider.frame = (0,self.height/2-7,self.width, 34)
		self.label.width, self.label.height = 46, 20
		self.label.y = self.slider.y - (self.label.height + 2)
		self.label.x = (self.slider.width - 34) * self.slider.value - (self.label.width/2) + 17
		
		
if __name__ == '__main__':
	#simple example with three sliders and a delegate to update the view name with the slider value.
	
	view = ui.View()
	
	class SliderValueChangeDelegate():
		def slider_value_did_change(self, value):
			view.name = str(value)
			
	value_change = SliderValueChangeDelegate()
	
	w = ui.get_screen_size()[0]
	a = SliderWithLabel(frame=(10,30,w-20,60), value=30, max_val=300)
	a.delegate = value_change
	b = SliderWithLabel(frame=(10,90,w-20,60), value=75, max_val=100)
	b.delegate = value_change
	c = SliderWithLabel(frame=(10,150,w-20,60), max_val=1000)
	c.delegate = value_change
	view.add_subview(a)
	view.add_subview(b)
	view.add_subview(c)
	view.background_color = 1
	view.present()

