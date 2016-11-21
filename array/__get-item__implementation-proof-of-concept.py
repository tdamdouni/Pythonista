# http://stackoverflow.com/questions/40694073/how-to-replicate-pandas-syntax-to-filter-data-frames

# You need to implement __getitem__ to take a list of booleans and only return items when True. You will also need to implement the conditional operators (>, ==, etc.) to return that list of booleans, e.g. (proof of concept code):

class A(object):
	def __init__(self, data):
		self.data = data
	def __getitem__(self, key):
		return A([d for k, d in zip(key, self.data) if k])
	def __gt__(self, value):
		return [d > value for d in self.data]
	def __repr__(self):
		return str(self.__class__) + ' [' + ', '.join(str(d) for d in self.data) + ']'
		
>>> a = A(list(range(20)))
>>> a
<class '__main__.A'> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
>>> a[a > 5]
<class '__main__.A'> [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

