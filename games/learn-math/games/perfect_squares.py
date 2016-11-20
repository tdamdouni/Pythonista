# coding: utf-8
'''Practice with both finding a number squared and finding the square root of perfect squares. All perfect squares will be less than or equal to 20*20.'''

import ui

class perfect_squares (ui.View):
	def __init__(self):
		self.question = ''
		self.multiple = 1
		
	def did_load(self):
		self.question = self.get_question()
		self['answer'].action = self.show_answer
		self['next'].action   = self.next_question
		self['question'].text = self.question[0]
		
	def touch_ended(self, touch):
		self.show_answer(None)
	
	def get_question(self):
		import random
		m = self['direction'].selected_index
		r = random.randint(2,20)
		s = r*r
		if m is 0: return (str(r), str(s))
		else:      return (str(s), str(r))
	
	def show_answer(self, sender):
		self['question'].text = self.question[1]
		
	def next_question(self, sender):
		self.question = self.get_question()
		self['question'].text = self.question[0]

if __name__ == '__main__':
	v = ui.load_view()
	v.present('sheet')
