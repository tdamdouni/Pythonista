# coding: utf-8
'''This game is played by determining what the sum of the opposite sides of the dice. The opposing sides of dice will always add up to 7. This game helps with keeping complex maths in you head.'''

import ui

class die (ui.View): 
	def __init__(self):
		self.number = None
		self._image = 'ionicons-record-32'
		self.configs = {
			1: ['middle'],
			2: ['top_left', 'bot_right'],
			3: ['top_left', 'middle', 'bot_right'],
			4: ['top_left', 'top_right', 'bot_left', 'bot_right'],
			5: ['top_left', 'top_right', 'bot_left', 'bot_right','middle'],
			6: ['top_left', 'top_right', 'mid_left', 'mid_right', 'bot_left', 'bot_right']
		}
	
	def roll_die(self):
		import random
		for dot in self.subviews:
			dot.image = None
		roll = random.randint(1,6)
		for dot in self.configs[roll]:
			self[dot].image = ui.Image.named(self._image)
		return roll
		
	def did_load(self):
		for dot in self.subviews:
			dot.image = None

class dice_game (ui.View):
	def __init__(self):
		self.dice = (0,0) 
		
	def did_load(self):
		self['answer'].action = self.show_answer
		self['next'].action   = self.roll_dice
		self.roll_dice('None')
		
	def touch_ended(self, touch):
		self.show_answer(None)
	
	def roll_dice(self, sender):
		d1 = self['die1'].roll_die()
		d2 = self['die2'].roll_die()
		self.dice = (d1,d2)
			
	@ui.in_background
	def show_answer(self, sender):
		from console import alert
		d1, d2 = self.dice
		answer = 14-(d1+d2)
		alert(str(answer), button1='Cool', hide_cancel_button=True)

if __name__ == '__main__':
	v = ui.load_view()
	v.present('sheet')
