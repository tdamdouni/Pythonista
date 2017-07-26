# https://gist.github.com/Phuket2/e93ff7fe3c7f6496f0e0461d5ace03a4

import ui

'''
	Forum user: @Phuket2
	licence: I will pay you to use it, license :)
	
	3 controls that just manipulate ui.Button's attrs
	
	This is more proof of concept rather than finished code.  
	
	I Normally try and make a class out of everything. a little stupid!
	Sometimes functions are very nice. a learning curve.
	
	not sure what you think, but the concept here, i think is quite nice.
	
	if you are good at python, i am sure you are saying something like,
	NO SHIT sherlock. 
	
	Anyway, i am still trying...
	
'''

def radio_button(width = 40, state = True):
	# radio button , just switches backgound images based on state
	# also adding state attr to ui.Button object
	# returns a real ui.Button
	
	# the function that action responds to...
	def action(sender):
		sender.state = not sender.state
		set_image(sender)
		
	def set_image(btn):
		if btn_imgs[int(btn.state)]:
			btn.background_image = ui.Image.named(btn_imgs[int(btn.state)])
		else: 
			btn.background_image = None
			
	btn_imgs = \
		['iob:ios7_circle_outline_32', 'iob:ios7_circle_filled_32']
	
	btn = ui.Button(name = 'rb')
	btn.width = width
	btn.height = width
	btn.corner_radius = btn.width / 2 # make it circular
	btn.state = state
	btn.border_width = .5
	
	btn.tint_color = 'blue'		# not working at the moment
	
	btn.action = action
	set_image(btn)
	return btn

def check_button(width = 40, state = True):
	# check button , just switches backgound images based on state
	# also adding state attr to ui.Button object
	# returns a real ui.Button
	
	# the function that action responds to...
	def action(sender):
		sender.state = not sender.state
		set_image(sender)
		
	def set_image(btn):
		if btn_imgs[int(btn.state)]:
			btn.background_image = ui.Image.named(btn_imgs[int(btn.state)])
		else: 
			btn.background_image = None
			
	# not using a image for False		
	btn_imgs = [None, 'iob:checkmark_32']

	btn = ui.Button(name = 'cb')
	btn.width = width
	btn.height = width
	btn.state = state
	btn.border_width = 1
	btn.tint_color = 'blue'		# not working at the moment
	btn.action = action
	set_image(btn)

	return btn
	
def letter_logo(text = 'IJ',
			font =('Arial Rounded MT Bold', 100), bg_color = 'teal'):
	
	# hmmm, not great. but still ok. size_to_fit not working as i would
	# expect it to. however, it could be me. 
	
	# this sort of icon/button/etc... used often in iOS
		
	# the function that action responds to...
	def action(sender):
		# not using it here... but could be a counter etc...
		pass
				
	btn = ui.Button(name = 'll')
	btn.font = font
	btn.title = text
	btn.alignment = ui.ALIGN_CENTER
	btn.border_width = .5
	btn.size_to_fit()
	btn.height = btn.width
	btn.width *= 1.3	# at the moment need to tweak these values
	btn.height *= 1.3	# at the moment need to tweak these values
	
	btn.corner_radius = btn.width / 2 # make it circular
	
	btn.bg_color = bg_color
	
	btn.tint_color = 'white'		# not working at the moment
	btn.border_color = 'yellow'
	
	btn.action = action
	
	return btn
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		btn = radio_button()
		btn.x = 100
		btn.y = 100
		self.add_subview(btn)
		
		btn = check_button(state = False)
		btn.x = 200
		btn.y = 100
		self.add_subview(btn)
		
		# test to call the buttons action method externally
		# for another idea
		btn.action(btn)
		
		btn = letter_logo()
		btn.x = 100
		btn.y = 200
		self.add_subview(btn)
		
		
if __name__ == '__main__':
	w = 300
	h = 400
	f = (0, 0, w, h)
	mc = MyClass(frame = f, bg_color = 'white', animated = False)
	mc.present('sheet')
	
