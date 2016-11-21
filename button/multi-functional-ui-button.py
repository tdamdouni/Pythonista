# https://forum.omz-software.com/topic/3424/share-multi-functional-ui-button

'''
    Pythonista Forum - @Phuket2
'''
import ui

def flip_button(img_on, img_off, state = False,
                is_circular = False, icon_size = 32, **kwargs):

	# pass at least a frame to ui.Button in case not passed in kwargs
	btn = ui.Button(frame = (0, 0, 40, 40))
	btn.state = state
	
	def btn_action(sender):
		sender.state = not sender.state
		sender.image = ui.Image.named(sender.images[sender.state])
		
	def rationalise_icon_size(img_name, icon_size):
		# not the best name for this function. but it attempts to
		# return the image_name of the icon_size, only 24,32,256.
		
		icon_check_list = [24, 32, 256]
		
		# only accept the std sizes
		if icon_size not in icon_check_list:
			return img_name
			
		for size in icon_check_list:
			if '_{}'.format(size) in img_name:
				return img_name.replace('_{}'.format(size),
				'_{}'.format(icon_size))
		return img_name
		
		
	img_on = rationalise_icon_size(img_on, icon_size)
	img_off = rationalise_icon_size(img_off, icon_size)
	btn.images = [img_off, img_on]
	
	btn.action = btn_action
	
	# apply the kwargs to the btn
	for k, v in kwargs.items():
		if hasattr(btn, k):
			setattr(btn, k, v)
			
	# just a resonable short cut to have a circular button.
	if is_circular:
		btn.corner_radius = btn.width / 2
		
	# set the initial state of the btn
	btn.image = ui.Image.named(btn.images[btn.state])
	
	return btn
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# tick mark
		btn = flip_button('iob:checkmark_32',
		'',
		state = False,
		is_circular = False,
		icon_size = 32,
		border_width = .5,
		x = 10,
		y = 10)
		self.add_subview(btn)
		
		# radio button
		btn = flip_button('iob:ios7_circle_filled_32',
		'iob:ios7_circle_outline_32',
		state = True,
		is_circular = True,
		icon_size = 32,
		tint_color = 'deeppink',
		x = 10,
		y = 100)
		
		self.add_subview(btn)
		
		# chevron idea
		btn = flip_button('iob:chevron_up_32',
		'iob:chevron_down_32',
		state = True,
		is_circular = True,
		icon_size = 24,
		tint_color = 'blue',
		border_width = .5,
		x = 10,
		y = 200)
		
		self.add_subview(btn)
		
		# can do many styles...
		
		
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	
	mc = MyClass(frame=f, bg_color='white', name = 'flip_button example')
	mc.present('sheet', animated=False)
# --------------------

