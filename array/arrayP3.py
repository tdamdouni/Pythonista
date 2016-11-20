# coding: utf-8

# https://gist.github.com/roger-/4192561

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
import numbers
import operator
import math
from six.moves import range
from six.moves import zip


class array(list):
	def __getitem__(self, y):
		if isinstance(y, (numbers.Integral, slice)):
			return list.__getitem__(self, y)
			
		if isinstance(y[0], bool):
			inds = (i for i, yi in enumerate(y) if yi)
			
			return array(list.__getitem__(self, i) for i in inds)
			
		if isinstance(y[0], numbers.Integral):
			return array(list.__getitem__(self, yi) for yi in y)
			
		raise TypeError
		
	def __setitem__(self, keys, y):
		if isinstance(keys, (numbers.Integral, slice)):
			return list.__setitem__(self, key, y)
			
		if isinstance(keys[0], bool):
			inds = (i for i, ki in enumerate(keys) if ki)
			
			if isinstance(y, numbers.Integral):
				for i in inds:
					list.__setitem__(self, i, y)
			else:
				for i, yi in zip(inds, y):
					list.__setitem__(self, i, yi)
					
			return
			
		if isinstance(keys[0], numbers.Integral):
			if isinstance(y, numbers.Integral):
				for i in keys:
					list.__setitem__(self, i, y)
			else:
				for i, yi in zip(keys, y):
					list.__setitem__(self, i, yi)
					
			return
			
		raise TypeError
		
	def __abs__(self):
		return array(abs(xi) for xi in self)
		
		
def elementwise_op(op_name, right=False):
	## get standard operator
	op = getattr(operator, '__' + op_name + '__')
	
	## element-wise replacement operator
	# left operators
	def new_l_op(self_, y):
		#print 'LOP'
		
		if isinstance(y, numbers.Number):
			return array(op(xi, y) for xi in self_)
		else:
			return array(op(xi, yi) for xi, yi in zip(self_, y))
			
	# right operators
	def new_r_op(self_, y):
		#print 'ROP'
		
		if isinstance(y, numbers.Number):
			return array(op(y, xi) for xi in self_)
		else:
			return array(op(yi, xi) for xi, yi in zip(self_, y))
			
	## replace standard operator
	if right:
		setattr(array, '__r' + op_name + '__', new_r_op)
	else:
		setattr(array, '__' + op_name + '__', new_l_op)
		
		
def patch_array():
	REPLACED_OPS = ['add', 'sub', 'mul', 'div', 'gt', 'ge', 'lt', 'le', 'pow', \
	'or', 'and', 'xor', 'truediv', 'mod']
	REPLACED_OPS2 = ['iadd', 'isub', 'imul', 'idiv', 'ipow', 'ior', 'iand', \
	'ixor', 'itruediv', 'imod']
	
	for op_name in REPLACED_OPS:
		elementwise_op(op_name)
		elementwise_op(op_name, right=True)
		
	for op_name in REPLACED_OPS2:
		elementwise_op(op_name)
		
patch_array()


def arange(*args, **kwargs):
	return array(range(*args, **kwargs))
	
def linspace(start, stop, num=50, endpoint=True, retstep=False):
	if num == 1:
		return array([start])
	elif num == 0:
		return array([])
		
	end_factor = 1 if endpoint else 0
	step = (stop - start)/(num - end_factor)
	space = arange(num)*step + start
	
	if retstep:
		return space, step
		
	return space
	
def zeros(num):
	return array([0]*num)
	
def ones(num):
	return array([1]*num)
	
def dot(x, y):
	return sum(xi*yi for xi, yi in zip(x, y))
	
	
def vectorize(func):
	if not hasattr(func, '__call__'):
		return func
		
	def new_func(x, *args, **kwargs):
		y = [func(xi, *args, **kwargs) for xi in x]
		
		return array(y)
		
	return new_func
	
def vectorize_all(namespace):
	for func in namespace.__dict__.keys():
		namespace.__dict__[func] = vectorize(namespace.__dict__[func])
		
		
vectorize_all(math)
from math import *

def main():
	x = arange(20)
	
	print(x[(x >= 5) & (x <= 15)])
	
	x[x > 5] += 4
	print(x[[6,7,11]])
	
	print(sin(linspace(0, 2*pi, 5)))
	print(linspace(0, 7, 5, retstep=True))
	
	
if __name__ == '__main__':
	main()

