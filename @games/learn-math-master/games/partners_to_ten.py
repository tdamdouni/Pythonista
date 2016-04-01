# coding: utf-8
'''Partners to ten are useful when doing any kind of math. In this game simply figure out what number, when added to the current number, will add up to 10.'''

import ui
	
class partners_to_ten (ui.View):
	def __init__(self):
		self.pairs = [(str(i),str(10-i)) for i in range(11)]
		self.pair  = self.get_pair()
	
	def did_load(self):
		self['answer'].action = self.show_answer
		self['next'].action   = self.next_pair
		self['number'].text   = self.pair[0]
		
	def touch_ended(self, touch):
		self.show_answer(None)
	
	def get_pair(self):
		import random
		return random.choice(self.pairs) 
	
	def show_answer(self, sender):
		self['number'].text = self.pair[1]
		
	def next_pair(self, sender):
		self.pair = self.get_pair()
		self['number'].text = self.pair[0]

if __name__ == '__main__':		
	v = ui.load_view()
	v.present('panel')
