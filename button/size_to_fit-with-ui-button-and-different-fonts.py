# https://forum.omz-software.com/topic/3216/size_to_fit-with-ui-button-and-different-fonts

import ui

def letter_logo(text = 'IJ',
            font =('Arial Rounded MT Bold', 50), bg_color = 'teal'):

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
	#btn.width *= 1.3   # at the moment need to tweak these values
	#btn.height *= 1.3  # at the moment need to tweak these values
	
	
	w=max(btn.height,btn.width)
	btn.height = btn.width = w
	
	w=btn.height/2+btn.width/2
	btn.height = btn.width = w
	
	btn.corner_radius = btn.width / 2 # make it circular
	
	btn.bg_color = bg_color
	
	btn.tint_color = 'white'        # not working at the moment
	btn.border_color = 'yellow'
	
	btn.action = action
	
	return btn
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		
		
		btn = letter_logo()
		btn.x = 10
		btn.y = 20
		self.add_subview(btn)
		
		btn = letter_logo(font = ('Avenir Next Condensed', 50))
		btn.x = 200
		btn.y = 20
		self.add_subview(btn)
		
		btn = letter_logo(font = ('Zapfino', 50))
		btn.x = 10
		btn.y = 150
		self.add_subview(btn)
		
if __name__ == '__main__':
	w = 300
	h = 400
	f = (0, 0, w, h)
	mc = MyClass(frame = f, bg_color = 'white', animated = False)
	mc.present('sheet')
	
# --------------------

