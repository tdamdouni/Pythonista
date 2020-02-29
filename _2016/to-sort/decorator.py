# coding: utf-8

# https://forum.omz-software.com/topic/3003/python-decorators-resource-not-a-question-just-a-resource

# https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize

from __future__ import print_function
def dump_args(func):
	"This decorator dumps out the arguments passed to a function before calling it"
	argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
	fname = func.func_name
	
	def echo_func(*args,**kwargs):
		print(fname, ":", ', '.join(
			'%s=%r' % entry
		for entry in zip(argnames,args) + kwargs.items()))
		return func(*args, **kwargs)
		
	return echo_func

