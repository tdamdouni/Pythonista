# https://forum.omz-software.com/topic/3537/lab-a-animated-ui-button-but-for-snippets

# Pythonista Forum - @Phuket2
import ui

# this function is the snippet
def pop_btn(*args, **kwargs):
	def pop_effect(sender, duration=.4, scale=1.25):
		x = y = scale
		
		def a():
			sender.transform = ui.Transform()
			
		def c():
			sender.enabled = True
			
		sender.transform = ui.Transform.scale(x, y)
		ui.animate(a, duration=duration, completion=c)
		
	def btn_action(sender):
		sender.enabled = False
		pop_effect(sender, scale=2)
		if sender.callback:
			sender.callback(sender)
			
	# do some normal initialisation
	btn = ui.Button(name='btn', frame=(0, 0, 100, 32))
	btn.title = btn.name
	btn.border_width = .5
	btn.callback = None
	btn.action = btn_action
	
	# if round = True is passed we make a round button
	round = kwargs.pop('round', False)
	if round:
		btn.corner_radius = btn.width / 2
		
	btn.callback = kwargs.pop('action', None)
	
	for k, v in kwargs.items():
		if hasattr(btn, k):
			setattr(btn, k, v)
			
	return btn
	
def dummy_action(sender):
	print('in dummy action', sender, sender.name)
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		
		btn = pop_btn(width=100, height=100,
		round=True, action=dummy_action, title='Hit Me',
		bg_color='teal', tint_color='white')
		
		btn.center = self.bounds.center()
		self.add_subview(btn)
		
if __name__ == '__main__':
	_use_theme = False
	w, h = 320, 480
	f = (0, 0, w, h)
	
	mc = MyClass(frame=f, bg_color='white')
	mc.present('sheet', animated=False)
# --------------------

