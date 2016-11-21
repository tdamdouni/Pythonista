# https://forum.omz-software.com/topic/3358/setting-attributes-for-a-custom-view-class-best-approach/15

#problem: passing some kwargs to use in an assignment loop may not work because, for example, a label and a view both use 'frame'. Here is a way to use different keyword arguments but assign to the correct attribute

#example: I could use 'label_frame' as an kwarg for the label.
#on setting the attribute it will set 'frame' as defined in the tuple (in defaults)

import ui
class ViewObject(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view(**kwargs)
		
	def make_view(self, **kwargs):
		label = self.make_label(**kwargs)
		self.add_subview(label)
		self.label = label
		
	def make_label(self, **kwargs):
		label = ui.Label()
		#defaults format: {<name for kwargs>: (<attribue name to set>, <value>)}
		defaults = {'label_bgcolor': ('background_color', 1),
		'label_border_color': ('border_color', 0.6),
		'label_border_width': ('border_width', 0.7),
		#'frame':('frame', (0,0,100,100)), #example: can't use 'frame' because the ui.View uses it...
		'label_frame': ('frame', (0,0,100,100))
		}
		for attr in defaults:
			setattr(label, defaults[attr][0], kwargs[attr]) if attr in kwargs else setattr(label, defaults[attr][0], defaults[attr][1])
		return label
		
a = ViewObject(background_color='#574854', frame=(0,0,201,205), label_bgcolor=0.3, label_frame=(0,0,40,40))
print('view background color', a.background_color)
print('view frame', a.frame)
print('background_color', a.label.background_color)
print('border_color', a.label.border_color)
print('border_width', a.label.border_width)
print('label frame', a.label.frame)

# --------------------

	def make_label(self, **kwargs):
		return ui.Label(**{
		'background_color': 1,
		'border_color': 0.6,
		'border_width': 0.7,
		'frame': (0, 0, 100, 100),
		**kwargs
		})
		
# --------------------

	def make_label(self, **kwargs):
		defaults = {'background_color': 1,  # create a dict of default values
		'border_color': 0.6,
		'border_width': 0.7,
		'frame': (0, 0, 100, 100)}
		for attr, value in kwargs.items():
			if attr.startswith('label_'):
				defaults[attr[len('label_'):]] = value
		return ui.Label(**defaults)         # return ui.Label w/ merged values
		
# --------------------

class MyClass(ui.View):
	def __init__(self, slider_args, label_args,  *args, **kwargs):
		super().__init__(*args, **kwargs)
		
if __name__ == '__main__':
	slider_kw = dict(bg_color = green)
	label_kw = dict(frame=(0, 0, 64, 32), bg_color = 'pink')
	v = MyClass(slider_args = slider_kw, label_ars = label_kw, bg_color = blue)
	
# --------------------

