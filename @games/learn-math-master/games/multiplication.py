# coding: utf-8
'''Trains you in simple multiplication. No number should be greater than 10.'''

import ui

class multiplication (ui.View):
	def __init__(self):
		self.question = self.get_question()
		
	def did_load(self):
		self['answer'].action = self.show_answer
		self['next'].action   = self.next_question
		
		self['question'].text = self.question[0]
		
	def touch_ended(self, touch):
		self.show_answer(None)
	
	def get_question(self):
		import random
		q = '%d * %d' % (random.randint(1,10), random.randint(1,10))
		a = eval(q)
		return (q.replace('*','×'),str(a))
	
	def show_answer(self, sender):
		self['question'].text = self.question[1]
		
	def next_question(self, sender):
		self.question = self.get_question()
		self['question'].text = self.question[0]

if __name__ == '__main__':
	v = ui.load_view()
	v.present('sheet')
