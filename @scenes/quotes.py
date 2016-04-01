# https://gist.github.com/kultprok/8711e0ffd4ae875284dd

# -*- coding: utf-8 -*-

from scene import *
from random import randrange, choice

class MyScene (Scene):
	def setup(self):
		self._changebackground()
		self._shownewquote()
		
	def _changebackground(self):
		background(randrange(50, 90)/100.0, 
		           randrange(50, 90)/100.0,
		           randrange(50, 90)/100.0)
	
	def _truncatestring(self, s, length=25):
		# Split into quote and author
		s, author = s
		# Truncate quote to fixed length, but
		# keeping word boundaries.
		output = []
		while len(s) > 0:
			if len(s) < length:
				output.append(s)
				break
			elif s[length - 1] == ' 'and len(s) > length:
				output.append(s[:length])
				s = s[length:]
			else:
				adjust = s[length:].find(' ')
				if adjust == -1:
					output.append(s)
					s = ''
				else:
					output.append(s[:length + adjust])
					s = s[length + adjust + 1:]
		# Strip all unnecessary blank spaces
		# from resulting strings.
		output = [line.strip() for line in output]
		# Righta-djust author and append to output
		w = max([len(data) for data in output])
		output.append(author.rjust(w))
		return '\n'.join(output)
		
	def _shownewquote(self):
		text(self._truncatestring(rq.next(), 20), x=self.size.w/2, y=self.size.h/2, font_name='DejaVuSansMono', font_size=12)
	
	def touch_began(self, touch):
		self._changebackground()
		self._shownewquote()

class RandomQuotes():
	def __init__(self):
		self.quotes = list(open('quotes.txt'))
		self.currentquote = self._newquote()

	def next(self):
		while True:
			next = self._newquote()
			if next != self.currentquote:
				self.currentquote = next
				break
		return self.currentquote
		
	def _newquote(self):
		 return choice(self.quotes).split('#-#')
		
if __name__ == '__main__':
	rq = RandomQuotes()
	run(MyScene())