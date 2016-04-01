class debugStream():
	""" create buffered output to speed up console printing"""
	def __init__(self):
		self.out = ''
		
	def push(self,string,*args):
		self.out += string.format(*args) + '\n'
	
	def send(self):
		print self.out
		self.out = ''
