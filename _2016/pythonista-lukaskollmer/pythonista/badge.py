# https://github.com/lukaskollmer/pythonista

"""
Use this module to access the app badge.
You can set a new value (int or str) or read the current value (int)
"""

__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"

from pythonista import _utils


# Application Badge String ----------------------------------------------------

def get():
	'''
	Get the badge value of the app icon on springboard
	
	Note: this only works with numerical badge values. Strings return 0 TODO: fix this
	'''
	_utils.guard_objc_util()
	
	return _utils._application.applicationIconBadgeNumber()

def set(value):
	'''
	Set the badge value of the app icon on springboard
	
	Accepts either a `str` or an `int`
	'''
	_utils.guard_objc_util()
	
	if isinstance(value, int):
		_utils._application.setApplicationIconBadgeNumber_(value)
	elif isinstance(value, str):
		_utils._application.setApplicationBadgeString_(value)

	
if __name__ == '__main__':
	#for m in dir(objc_util.UIApplication.sharedApplication()):
		#print(m)
	set('lk')
	set(0)
	print('get_badge: {}'.format(get()))
	
