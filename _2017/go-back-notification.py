# https://forum.omz-software.com/topic/4138/getting-notification-on-navigationview-go-back/4

import ui

about = '''Press "Tap me" and then back ("<" in the upper left) numerous times.
           Desired behavior: Colors remain constant (white, red, white, red)
           Actual behavior: Colors cycle forward (white, red, white, green)'''

colors = 'white red green blue grey'.split()


class ColorView(ui.View):
	def __init__(self):
		self.index = 0
		self.name = 'white'
		self.add_subview(self.make_button())
		frame = (0, -220, *(ui.get_screen_size()))
		self.add_subview(ui.Label(text=about, frame=frame, number_of_lines=0))
		
	def button_tapped(self, sender):
		sender.navigation_view.push_view(self.make_button())
		
	def go_back(self):  # this NEVER gets called :-(
		self.index -= 1
		
	def layout(self):
		self.subviews[0].frame = self.bounds
		
	def make_button(self):
		color = colors[self.index % len(colors)]
		self.index += 1
		return ui.Button(title='Tap me', action=self.button_tapped, bg_color=color, name=color)
		
		
ui.NavigationView(ColorView()).present()

