#!/usr/bin/env python3
# Copyright 2016 Lukas Kollmer<lukas@kollmer.me>
# Code adopted for Pythonista from http://stackoverflow.com/a/6145556/2513803

__all__ = ['get_log']

from ctypes import *
from objc_util import *
import time

c = cdll.LoadLibrary(None)

asl_new = c.asl_new
asl_new.restype = c_void_p
asl_new.argtypes = [c_uint32]

asl_search = c.asl_search
asl_search.restype = c_void_p
asl_search.argtypes = [c_void_p, c_void_p]

aslresponse_next = c.aslresponse_next
aslresponse_next.restype = c_void_p
aslresponse_next.argtypes = [c_void_p]

asl_key = c.asl_key
asl_key.restype = c_char_p
asl_key.argtypes = [c_void_p, c_uint32]

asl_get = c.asl_get
asl_get.restype = c_char_p
asl_get.argtypes = [c_void_p, c_char_p]

aslresponse_free = c.aslresponse_free
aslresponse_free.restype = None
aslresponse_free.argtypes = [c_void_p]


ASL_TYPE_QUERY = 0 #c_uint32

def get_log():
	
	logs = []
	
	
	q, m = None, None #aslmsg
	
	q = asl_new(ASL_TYPE_QUERY)
	
	r = asl_search(None, q) #aslresponse
	
	m = aslresponse_next(r)
	while m != None:
		tmpDict = NSMutableDictionary.dictionary()
		
		i = c_uint(0)
		key = asl_key(m, i)
		while key != None:
			
			keyString = NSString.stringWithUTF8String_(key)
			val = asl_get(m, key)
			
			valString = NSString.stringWithUTF8String_(val)
			
			tmpDict.setObject_forKey_(valString, keyString)
			
			# continue while statement
			i = c_uint(i.value + 1)
			key = asl_key(m, i)
		logs.append(tmpDict)
			
			
		# continue while statement
		m = aslresponse_next(r)
	aslresponse_free(r)
	return logs

if __name__ == '__main__':
	import console
	import ui
	import editor
	import dialogs	
	
	items = []
	
	for log in get_log():
		items.append('{} - {}'.format(log['CFLog Local Time'], log['Message']))
	
	log_text = '\n'.join(items)
	
	def share(sender):
		dialogs.share_text(log_text)
	
	theme = editor.get_theme_dict()
	
	view = ui.TextView()
	view.name = 'Pythonista System Log'
	view.text = log_text
	view.font = ('Menlo-Regular', 15)
	view.editable = False
	
	share_button = ui.ButtonItem(title='Share', action=share)
	view.right_button_items = [share_button]
	
	editor.present_themed(view)
