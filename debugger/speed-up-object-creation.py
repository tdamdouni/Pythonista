# coding: utf-8

# https://forum.omz-software.com/topic/3093/slow-autocomplete-for-complex-objects/13

def getattribstrings(o):
	A=[]
	itstype=type(o)
	for a in dir(o):
		if hasattr(itstype,a):
			if callable(getattr(itstype,a)):
				A.append(a+'()')
			else:
				A.append(a)
		else:
			if callable(getattr(o,a)):
				A.append(a+'()')
			else:
				A.append(a)
	return A

