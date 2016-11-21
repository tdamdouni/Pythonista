#coding: utf-8
'''This game helps with learning basic times tables.'''

import ui

class multiples_of (ui.View):
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
		m = self['multiples'].selected_index+1
		q = '%d * %d' % (random.randint(1,12), m)
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
