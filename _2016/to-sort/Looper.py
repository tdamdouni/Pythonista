# coding: utf-8

# https://forum.omz-software.com/topic/1465/help-typeerror-expected-callable-function/7

import sys

def looper(i=1):
	try:
		looper(i+1)
	except RuntimeError as err:
		print('{}/{} {}'.format(i, sys.getrecursionlimit(), err))
		
looper()

