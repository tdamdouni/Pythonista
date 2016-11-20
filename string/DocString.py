# coding: utf-8

# https://forum.omz-software.com/topic/2412/share-code-doc-strings-from-a-class

def get_docstrings_for_class(class_obj):
	'''
	return the doc string or None
	For each attr in the passed class,
	if the attr does not startwith('_') and its callable
	return a tuple(attr, __doc__)
	in this case you expect attr to be a method
	of the class
	'''
	return [ (attr, getattr(class_obj, attr).__doc__) for attr  in dir(class_obj) if not attr.startswith('_') and callable(getattr(class_obj, attr))]
	#return [ (attr, getattr(class_obj, attr).__doc__) for attr  in
	#list(dir(class_obj).append('{}.__doc__'.format(str(class_obj))))
	#if not attr.startswith('_') or attr == '__init__' and callable(getattr(class_obj, attr))]
	
if __name__ == '__main__':
	#ds = get_docstrings_for_class(tuple)
	#print '\n'.join( '{h} {0} {h}\n {1}\n'.format(tp[0], tp[1], h = '#' * 5)
	#can be rewritten as:
	print('\n'.join('{h} {} {h}\n {}\n'.format(*tp, h = '#' * 5))   # ;-)
	for tp in get_docstrings_for_class(str))

