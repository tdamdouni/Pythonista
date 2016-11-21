#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2906/ui-elements-creation

import ui

def do_kwargs(obj, *args, **kwargs):
	for k, v in kwargs.iteritems():
		if hasattr(obj, k):
			setattr(obj, k, v)
	return obj
	
def Button(*args, **kwargs):
	return do_kwargs(ui.Button(), *args, **kwargs)
	
if __name__ == '__main__':
	btn = Button(title = 'Go', bg_color = 'purple')
	#btn = Button(title = 'Ian')
	btn.present('sheet')

