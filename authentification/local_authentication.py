# coding: utf-8

# https://gist.github.com/bmw1821/d44b83d80f2f77e4f832

from objc_util import * 
import time

def authenticate(reason = ' '):
	ObjCClass('NSBundle').bundleWithPath_('/System/Library/Frameworks/LocalAuthentication.framework').load()
	context = ObjCClass('LAContext').alloc().init()
	
	global result
	result = None
	retain_global(result)
	
	def auth_response_handler(_cmd, success, _error):
		global result
		if success:
			result = True
		else:
			error = ObjCInstance(_error)
			if error.code() == -2:
				result = False
	
	auth_response_handler_block = ObjCBlock(auth_response_handler, None, [c_void_p, c_void_p, c_void_p])
	
	reason = str(reason) or ' '
	#if reason == '':
		#reason = ' '
	
	context.evaluatePolicy_localizedReason_reply_(2, reason, auth_response_handler_block)
	
	while result == None:
		pass
	
	return result
