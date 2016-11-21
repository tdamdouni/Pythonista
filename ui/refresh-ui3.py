# https://forum.omz-software.com/topic/3589/refresh-ui/5

# Pythonista Forum - @Phuket2
import ui, editor

# get the numbered spades and Hearts cards (images)
img_list = ['card:Spades' + str(i) for i in range(2, 11)] + ['card:Hearts' + str(i) for i in range(2, 11)]

class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.img_rect = (0, 0, 200, 300)
		self.img_num = 0
		self.make_view()
		
	def make_view(self):
		btn = ui.Button(frame=(0, 0, 32, 100))
		btn.title = 'Stop'
		btn.size_to_fit()
		btn.center = self.bounds.center()
		btn.y = self.height - btn.height - 10
		btn.action = self.btn_stop
		self.add_subview(btn)
		self.start()
		
	def start(self):
		# ui.Delay, continually calls this method, until the stop button
		# is pressed or the view will close
		self.set_needs_display()
		ui.delay(self.start, .8)
		
		if self.img_num == len(img_list)-1:
			self.img_num = 0
		else:
			self.img_num += 1
			
	def draw(self):
		r = ui.Rect(*self.img_rect)
		r.center(self.bounds.center())
		ui.Image.named(img_list[self.img_num]).draw(*r)
		
	def btn_stop(self, sender):
		self.name = 'delay is stopped'
		ui.cancel_delays()
		
	def will_close(self):
		ui.cancel_delays()
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 600, 800
	f = (0, 0, w, h)
	style = 'sheet'
	
	mc = MyClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present(style=style, animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=False)

