#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2412/share-code-doc-strings-from-a-class/12

from __future__ import print_function
def foo(lst):
	return [i for i in lst + ['4', '5', '6']]
	
def bar(lst):
	newlist = lst + ['4', '5', '6']
	ret_list = []
	for i in newlist:
		ret_list.append(i)
		
	return ret_list
	
lst = list(['1','2', '3'])
print(foo(lst))
print(bar(lst))
assert foo(lst) == bar(lst), 'Huston we have a problem'

