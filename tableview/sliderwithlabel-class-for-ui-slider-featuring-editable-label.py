# https://forum.omz-software.com/topic/3353/share-code-sliderwithlabel-class-for-ui-slider-featuring-editable-label/16

import ui

class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# def instance vars
		self.slider = None
		#etc...
		self.make_view(**kwargs)
		
	def make_view(self, **kwargs):
		slider = ui.Slider()
		slider.bg_color = 'green'
		#etc
		self.add_subview(slider)
		self.slider = slider
		
	def layout(self):
		r = ui.Rect(*self.bounds.inset(5, 5))
		
		self.slider.width = r.width
		self.slider.x = r.x
		self.slider.y = r.y
		
	def draw(self):
		# only should overide draw if you acually need to use it
		# here only illustration purposes.
		pass
		
if __name__ == '__main__':
	v = MyClass(frame = (0, 0, 600, 800), bg_color = 'white')
	v.present('sheet')
	
# --------------------

# returns any kwargs that are not attrs in ui.View

#def get_non_uiview_kwargs(self, **kwargs):
#       return set(kwargs) - set(ui.View.__dict__)

