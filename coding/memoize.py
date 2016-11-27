# https://gist.github.com/Subject22/6d340d7e2ef9a8f3ff1b49c48af57e7e

class memoize(dict):
	def __init__(self, func):
		self.func = func
		
	def __call__(self, *args):
		return self[args]
		
	def __missing__(self, args):
		result = self[args] = self.func(*args)
		return result

