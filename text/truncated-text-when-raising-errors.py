# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2483/truncated-text-when-raising-errors_

try:
    #code that raises the error
except Exception, e:
	print e
	
###==============================

if not all(k in pyui_rec for k in pyui_descriptor):
	err_str = '''the pyui_rec does not contain
	all the keys check dict - pyui_descriptor {}'''
	raise TypeError(err_str.format(pyui_descriptor))
	
###==============================

print err_str.format(pyui_descriptor)

