# coding: utf-8

# https://gist.github.com/ejetzer/819c6d7ddd721467f72e

import numbers, decimal, fractions, sympy, itertools

def permutations(p):
	res = set()
	for i in range(len(p)):
		for q in itertools.permutations(p, i):
			res.add(q)
	return res
	
def compose(funcs):
	def final(arg):
		res = arg
		for func in funcs:
			res = func(res)
		return res
	return final
	
class ThingWithErrors (object):

	wrapped_thing = str
	
	def __init__(self, value, errors=[], wrongs={}):
		self.value = type(self).wrapped_thing(value)
		self.errors = errors
		self.wrongs = wrongs
		
	def __propagate__(self, other, func):
		wrongs = {}
		a, b = self.value, getattr(other, 'value', other)
		for left in list(self.wrongs.items()) + [(a, [])]:
			for right in list(getattr(other, 'wrongs', {}).items()) + [(b, [])]:
				for left_error in permutations(self.errors + [lambda x: (x, [])]):
					for right_error in permutations(getattr(other, 'errors', []) + [lambda x: (x, [])]):
						# Now only one error is applied per step.
						# How can I apply more than one at a time,
						# going through all combinations of errors?
						print left, right
						le, re = compose(left_error)(left[0]), compose(right_error)(right[0])
						print le, re
						result = func(le[0], re[0])
						print result
						wrong = left[1] + right[1] + le[1] + re[1]
						wrongs[result] = wrongs.get(result, []) + wrong
						result = func(left[0], re[0])
						wrong = left[1] + right[1] + re[1]
						wrongs[result] = wrongs.get(result, []) + wrong
						result = func(le[0], right[0])
						wrong = left[1] + right[1] + le[1]
						wrongs[result] = wrongs.get(result, []) + wrong
		value = self.value + getattr(other, 'value', other)
		errors = self.errors + getattr(other, 'errors', [])
		return type(self)(value, errors, wrongs)
		
	def __getattr__(self, attr):
		return lambda s, o: s.__propagate__(o, getattr(s.wrapped_thing, attr))
		
	def __repr__(self):
		return repr(self.value)
		
class NumberWithErrors (ThingWithErrors, numbers.Number):

	wrapped_thing = float
	
	def __add__(self, other):
		print other, self
		return self.__propagate__(other, lambda x,y: x+y)
		
	def __radd__(self, other):
		return self.__propagate__(other, lambda x,y: y+x)
		
	def __sub__(self, other):
		return self.__propagate__(other, lambda x,y: x-y)
		
	def __rsub__(self, other):
		return self.__propagate__(other, lambda x,y: y-x)
		
class DecimalWithErrors (NumberWithErrors):
	wrapped_thing = decimal.Decimal
	
class FractionWithErrors (NumberWithErrors):
	wrapped_thing = fractions.Fraction
	
class SymbolWithErrors (NumberWithErrors):

	def __init__(self, value, errors=[], wrongs={}):
		self.value = sympy.sympify(value)
		self.errors = errors
		self.wrongs = wrongs
		
def sign_error(x):
	print x
	ans = -x
	return ans, ['You may have switched the sign of ${}$ (sign-error).'.format(x)]
	
def forgotten_error(x):
	return 0, ['You may have forgotten ${}$, & replaced it by a $0$.'.format(x)]
	
errors = [sign_error, forgotten_error]

a, b = SymbolWithErrors('x', errors), SymbolWithErrors(3, errors)
print 'a, b =', a, b

c = a + b
print 'c =', c
print 'c.wrongs =', c.wrongs

d = c + b
print 'd =', d

