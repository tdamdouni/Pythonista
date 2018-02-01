# https://forum.omz-software.com/topic/4332/set-a-gradient-as-a-background/3

import ui

class MyView(ui.View):
	def __init__(self, gradient, *args, **kwargs):
		self.gradient = gradient
		super().__init__(*args, **kwargs)
		self.step_size = 3
		
	def draw(self):
		x,y,w,h = self.frame
		((fr,fg,fb), (tr, tg, tb)) = gradient
		num_steps = int(w/self.step_size)
		for step in range(num_steps):
			x = step*self.step_size
			t = step/num_steps
			path = ui.Path.rect(x,0,self.step_size,h)
			ui.set_color((fr*(1-t)+tr*t, fg*(1-t)+tg*t, fb*(1-t)+tb*t))
			path.fill()
		path = ui.Path.rect(num_steps*self.step_size, 0, w-num_steps*self.step_size, h)
		ui.set_color((tr,tg,tb))
		path.fill()
		
		
w,h = 400,400
gradient = ((1,0,0) , (0,1,0))
v = MyView(gradient, frame=(0,0,w,h))
v.present('sheet')

