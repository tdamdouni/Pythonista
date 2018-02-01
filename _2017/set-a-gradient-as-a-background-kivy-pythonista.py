# https://forum.omz-software.com/topic/4332/set-a-gradient-as-a-background/4

def getgui():
	try:
		import ui
		platform = 'Pythonista'
		gui = ui.View
	except:
		try:
			from kivy.uix.floatlayout import FloatLayout
			platform = 'Kivy'
			gui = object
		except:
			from Tkinter import Tk
			platform = 'Tk'
			gui = object
	return platform, gui
	
platform, gui = getgui()

if platform == 'Pythonista':
	import ui
	
class MyView(gui):
	def __init__(self, platform, gradient, *args, **kwargs):
		self.gradient = gradient
		self.step_size = 3
		self.gradient_type = ['linear', 'radial', 'square']
		self.current_fill = 0
		self.grads = []
		self.platform = platform
		if self.platform == 'Pythonista':
			ui.View.__init__(self, *args, **kwargs)
			self.next_button = ui.Button(frame= \
			(330, 360, 30, 60), title = 'Next')
			self.next_button.background_color = (0.4,0.4,0.4)
			self.next_button.action = self.next_fill
			self.next_button.height = 30
			self.next_button.width = 60
			self.next_button.tint_color = 'white'
			self.next_button.font = ('<system>', 12)
			self.add_subview(self.next_button)
			
		elif self.platform == 'Kivy':
			from kivy.uix.floatlayout import FloatLayout
			from kivy.uix.button import Button
			self.root = FloatLayout()
			self.frame = kwargs['frame']
			self.next_button = Button( text = 'NEXT',
			size_hint_y = None, size_hint_x = None,
			height = 30, width = 60, font_size = 12, pos = (330, 10),
			on_press = self.next_fill )
			self.root.add_widget(self.next_button)
			
		elif self.platform == 'Tk':
			from Tkinter import Tk
			from Tkinter import Canvas
			from Tkinter import Frame
			from Tkinter import Label
			from Tkinter import NW
			self.master = Tk()
			self.root = Canvas(self.master, width=kwargs['frame'][2], \
			height=kwargs['frame'][3])
			self.root.pack()
			self.frame = kwargs['frame']
			contour = Frame(self.master, height=30, width=60)
			contour.pack_propagate(0) # don't shrink
			label = Label(contour, text='NEXT', fg='white', bg='#585858', \
			height=30, width=60)
			label.bind("<Button-1>", self.tk_button_down)
			label.bind("<ButtonRelease-1>", self.tk_button_up)
			
			label.pack()
			label.config(font=('TkDefaultFont',12), padx=0,pady=0)
			contour.place(x=330, y =360, anchor=NW)
			
	def next_fill(self, sender):
		self.current_fill += 1
		if self.current_fill == 3:
			self.current_fill = 0
		if self.platform == 'Pythonista':
			self.set_needs_display()
		else:
			self.draw()
			
	def tk_button_down(self, event):
		event.widget.config(bg='#00A5D4')
		
	def tk_button_up(self, event):
		event.widget.config(bg='#585858')
		self.next_fill(self.tk_button_up)
		
	def present_all(self, mode):
		if self.platform == 'Pythonista':
			self.present(mode)
		if self.platform == 'Tk':
			self.draw()
			self.root.mainloop()
		elif self.platform == 'Kivy':
			from kivy.base import runTouchApp
			from kivy.core.window import Window
			Window.size = self.frame[2:4]
			self.draw()
			runTouchApp(self.root)
			
	def draw(self):
		x,y,w,h = self.frame
		((fr,fg,fb), (tr, tg, tb)) = gradient
		num_steps = int(w/self.step_size)
		for step in range(num_steps):
			x = step*self.step_size
			t = step/(num_steps * 1.0)
			if self.platform == 'Pythonista':
				if self.gradient_type [self.current_fill] == 'linear':
					path = ui.Path.rect(x,0,self.step_size,h)
				elif self.gradient_type [self.current_fill] == 'radial':
					if w - ((2 * step) * self.step_size) >= 0:
						path = ui.Path.oval(x, x, w - 2*x, h-2*x)
				elif self.gradient_type [self.current_fill] == 'square':
					if w - ((2 * step) * self.step_size) >= 0:
						path = ui.Path.rect(x,x,w - ((2*step) * \
						(self.step_size)),h - (2*step)*self.step_size)
					ui.set_color((fr*(1-t)+tr*t, fg*(1-t)+tg*t, fb*(1-t)+tb*t))
					path.fill()
				ui.set_color((fr*(1-t)+tr*t, fg*(1-t)+tg*t, fb*(1-t)+tb*t))
				path.fill()
				
			elif self.platform == 'Tk':
				if step == 0:
					self.root.create_rectangle( 0, 0, w, h, \
					fill='black', outline='black')
				cl = '#' + '%02x' % int((fr*(1-t)+tr*t) * 255) + \
				'%02x' % int((fg*(1-t)+tg*t) * 255) + \
				'%02x' % int((fb*(1-t)+tb*t) * 255)
				if self.gradient_type [self.current_fill] == 'linear':
					self.root.create_rectangle( x, 0, self.step_size + x, h, \
					fill=cl, outline=cl)
				elif self.gradient_type [self.current_fill] == 'radial':
					if w - ((2 * step) * self.step_size) >= 0:
						self.root.create_oval( x + self.step_size, x + \
						self.step_size, w - ((2*step) * (self.step_size)) \
						+ x, h - (2*step)*self.step_size + x, \
						fill=cl, outline=cl)
				elif self.gradient_type [self.current_fill] == 'square':
					if w - ((2 * step) * self.step_size) >= 0:
						self.root.create_rectangle( x, x, w - ((2*step) * \
						(self.step_size)) + x, h - (2*step)*self.step_size \
						+ x, fill=cl, outline=cl)
						
			elif self.platform == 'Kivy':
				if step == 0:
					from kivy.graphics import Color
					from kivy.graphics import Rectangle
				self.grads.append ((fr*(1-t)+tr*t, fg*(1-t)+tg*t, \
				fb*(1-t)+tb*t))
				self.root.canvas.add(Color (fr*(1-t)+tr*t, fg*(1-t)+tg*t, \
				fb*(1-t)+tb*t))
				if self.gradient_type [self.current_fill] == 'linear':
					self.root.canvas.add(Rectangle(pos = (x, 0), \
					size = (self.step_size,h)))
				elif self.gradient_type [self.current_fill] == 'radial':
					if w - ((2 * step) * self.step_size) >= 0:
						if step == 0:
							from kivy.graphics import Line
						self.root.canvas.add(Line(circle = (w/2, h/2, w - \
						(2*step)*self.step_size), width = self.step_size))
				elif self.gradient_type [self.current_fill] == 'square':
					if w - ((2 * step) * self.step_size) >= 0:
						self.root.canvas.add(Rectangle(pos = (x, x), size = \
						(w - (2*step)*self.step_size, \
						h - (2*step)*self.step_size)))
				self.root.remove_widget(self.next_button)
				self.root.add_widget(self.next_button)
				
w,h = 400,400
gradient = ((1,0,0) , (0,1,0))
v = MyView(platform,gradient, frame=(0,0,w,h))
v.present_all('sheet')

