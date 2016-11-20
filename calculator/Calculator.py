from __future__ import division
from scene import *
from math import sqrt, pi
import sound

button_pad = [['ans', 'pi', 'sqrt(', '%'],
              ['(', ')', '*', '/'],
              ['7', '8', '9', '-'],
              ['4', '5', '6', '+'],
              ['1', '2', '3', '='],
              ['0', '.', '<--', 'c']]

class Calculator (Scene):
	def setup(self):
		sound.set_volume(1)
		self.root_layer = Layer(self.bounds)
		self.user_input = {'ans':'', 'text':''}
		self.buttons = []
		self.create_buttons()
	
	def create_buttons(self):
		width, height = self.size
		for y in xrange(len(button_pad)):
			for x in xrange(len(button_pad[y])):
				w = (width)/len(button_pad[y])
				h = (height-height/5)/len(button_pad)
				r = Rect(x * w, (height-height/5-h)-(y*h), w, h)
				button = Button(r, button_pad[y][x])
				if button_pad[y][x] != ' ':
					button.txt = button_pad[y][x]
				self.buttons.append(button)
		for button in self.buttons:
			button.touched = False
			self.root_layer.add_layer(button)
			
	def calculate(self):
		try: 
			self.user_input['ans'] = str(eval(self.user_input['text']))
			self.user_input['text'] = self.user_input['ans']
		except Exception as e:
			pass 
	
	def draw(self):
		width, height = self.size
		background(1,1,1)
		text(str(self.user_input['text']), x=width, y=height-height/6.7, font_size=height/20, alignment=4)
		for button in self.buttons:
			button.draw()
	
	def touch_began(self, touch):
		for button in self.buttons:
			if touch.location in button.frame:
				button.touch_began(touch)
	
	def touch_moved(self, touch):
		for button in self.buttons:
			button.touch_moved(touch)
			
	def touch_ended(self, touch):
		for button in self.buttons:
			button.touch_ended(touch)
			if touch.location in button.frame:
				button.touched = True
			if button.touched:
				sound.play_effect('Click_1')
				if button.txt == 'c':
					self.user_input['text'] = ''
				elif button.txt == '<--':
					self.user_input['text'] = self.user_input['text'][:-1]
				elif button.txt == 'ans':
					self.user_input['text'] += self.user_input['ans']
				elif button.txt == '%':
					try:
						self.user_input['ans'] = str(eval(self.user_input['text'])/100)
						self.user_input['text'] = self.user_input['ans']
					except SyntaxError as e:
						pass  
				elif button.txt == '=':
					self.calculate()
				else: 
					try: 
						self.user_input['text'] += button.txt
					except AttributeError:
						pass 
			button.touched = False 

run(Calculator())
