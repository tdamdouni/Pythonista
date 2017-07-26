# # https://github.com/lukaskollmer/pythonista

"""
Use this module to register custom keyboard commands
"""

__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"

from pythonista import _utils

_utils.guard_objc_util()

import objc_util
import ctypes
import swizzle


objc_getAssociatedObject = objc_util.c.objc_getAssociatedObject
objc_getAssociatedObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
objc_getAssociatedObject.restype = ctypes.c_void_p

objc_setAssociatedObject = objc_util.c.objc_setAssociatedObject
objc_setAssociatedObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
objc_setAssociatedObject.restype = None

NSArray = objc_util.ObjCClass("NSArray")
NSMutableArray = objc_util.ObjCClass("NSMutableArray")
UIKeyCommand = objc_util.ObjCClass('UIKeyCommand')

associated_obj_key = objc_util.ns("lk_custom_key_commands")

_UIKeyModifierAlphaShift = 1 << 16
_UIKeyModifierShift      = 1 << 17
_UIKeyModifierControl    = 1 << 18
_UIKeyModifierAlternate  = 1 << 19
_UIKeyMofifierCommand    = 1 << 20
_UIKeyModifierNumericPad = 1 << 21


_modifiers_map = {
	"cmd":      _UIKeyMofifierCommand,
	"capslock": _UIKeyModifierAlphaShift,
	"shift":    _UIKeyModifierShift,
	"control":  _UIKeyModifierControl,
	"option":      _UIKeyModifierAlternate,
	"num":      _UIKeyModifierNumericPad
}

def register(shortcut, action=None, title=None):
	"""
	Note: this shortcut works only when the editor is in focus. (no idea why)
	For some reason i, b, u dont work (http://www.openradar.me/25463955p\)
	"""
	
	
	if isinstance(shortcut, objc_util.ObjCInstance):
		if shortcut.isKindOfClass_(UIKeyCommand):
			_add_custom_command(shortcut)
			return shortcut
	keys = shortcut.split("+")
	_modifiers = keys[:-1]
	input = keys[-1].upper()
	
	modifiers = (0 << 00)
	for modifier in _modifiers:
		modifiers |= _modifiers_map[modifier.lower()]
	
	
	selector = _utils.add_method(action, _utils._application)
	keyCommand = UIKeyCommand.keyCommandWithInput_modifierFlags_action_discoverabilityTitle_(input, modifiers, selector, title)
	
	_add_custom_command(keyCommand)
	return keyCommand

def deregister(command):
	existing_custom_commands = _get_custom_commands()
	existing_custom_commands.removeObject_(command)
	save_custom_commands(existing_custom_commands)

def _get_custom_commands():
	existing_custom_commands = objc_getAssociatedObject(_utils._application, associated_obj_key)
	try:
		# This is a terrible solution, but it's the only way I could come up with
		# to check if the object is `nil` (not empty!)
		# checking if it's None wont work, no idea why.
		# The idea is that this will fail since the __str__ method will try to load
		# the description, which of course is nil, since the object itself is nil
		s = objc_util.ObjCInstance(existing_custom_commands).__str__()
	except:
		existing_custom_commands = objc_util.ns([])
	return objc_util.ObjCInstance(existing_custom_commands)

def save_custom_commands(commands):
	objc_setAssociatedObject(_utils._application, associated_obj_key, commands, 1)

def _add_custom_command(command):
	existing_custom_commands = _get_custom_commands()
	existing_custom_commands.addObject_(command)
	save_custom_commands(existing_custom_commands)

def keyCommands(_self, _sel):
	commands = _get_custom_commands()
	commands.addObjectsFromArray_(_utils._application.originalkeyCommands())
	return commands.ptr


# Even though the script will be imported multiple times, we should swizzle only once
if not "originalkeyCommands" in dir(_utils._application):
	app = _utils._application
	cls = objc_util.ObjCInstance(objc_util.c.object_getClass(app.ptr))
	swizzle.swizzle(cls, 'keyCommands', keyCommands)


if __name__ == "__main__":
	def handler(_self, _cmd):
		print("ACTION")
	
	c = register("cmd+option+U", handler, "ACTION")
	print(_get_custom_commands())
	#deregister(c)

