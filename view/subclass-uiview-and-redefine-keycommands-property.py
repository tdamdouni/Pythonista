from __future__ import print_function
# https://forum.omz-software.com/topic/2049/possible-to-subclass-uiview-and-redefine-keycommands-property/7

from objc_util import *
from random import random
import ui

UIKeyCommand = ObjCClass('UIKeyCommand')

def keyCommands(_self, _cmd):
	cmd_key_flag = (1<<20)
	key_command = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('R', cmd_key_flag, 'keyCommandAction')
	commands = ns([key_command])
	return commands.ptr
	
def canBecomeFirstResponder(_self, _cmd):
	return True
	
def keyCommandAction(_self, _cmd):
	self = ObjCInstance(_self)
	r, g, b = random(), random(), random()
	self.setBackgroundColor_(UIColor.colorWithRed_green_blue_alpha_(r, g, b, 1))
	
KeyCommandsView = create_objc_class('KeyCommandsView', UIView, [keyCommands, canBecomeFirstResponder, keyCommandAction])

@on_main_thread
def main():
	main_view = ui.View(frame=(0, 0, 400, 400))
	main_view.name = 'Key Commands Demo'
	
	v = KeyCommandsView.alloc().initWithFrame_(((0, 0), (400, 400)))
	v.setBackgroundColor_(UIColor.lightGrayColor())
	v.becomeFirstResponder()
	ObjCInstance(main_view).addSubview_(v)
	
	label = ui.Label(frame=(0, 0, 400, 400))
	label.alignment = ui.ALIGN_CENTER
	label.text = 'Press Cmd+R on an external keyboard to change the background color.'
	label.number_of_lines = 0
	main_view.add_subview(label)
	
	main_view.present('sheet')
	
if __name__ == '__main__':
	main()
# --------------------

# coding: utf-8
from objc_util import *
from random import random
import ui

UIKeyCommand = ObjCClass('UIKeyCommand')

modifiers = {(1<<17): 'Shift', (1<<18): 'Ctrl', (1<<19): 'Alt', (1<<20): 'Cmd', (1<<21): 'NumPad'}

def keyCommands(_self, _cmd):
	cmd_key_flag = (1<<20)
	key_command_r = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('R', cmd_key_flag, 'keyCommandAction:')
	key_command_b = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('B', cmd_key_flag, 'keyCommandAction:')
	commands = ns([key_command_r, key_command_b])
	return commands.ptr
	
def canBecomeFirstResponder(_self, _cmd):
	return True
	
def keyCommandAction_(_self, _cmd, _sender):
	self = ObjCInstance(_self)
	key_cmd = ObjCInstance(_sender)
	flags = key_cmd.modifierFlags()
	modifier_str = ' + '.join(modifiers[m] for m in modifiers.keys() if (m & flags))
	key_input = key_cmd.input()
	print('Input: "%s" Modifiers: %s' % (key_input, modifier_str))
	if str(key_input) == 'R':
		r, g, b = random(), random(), random()
	else:
		r, g, b = 0.0, 0.0, 1.0
	self.setBackgroundColor_(UIColor.colorWithRed_green_blue_alpha_(r, g, b, 1))
	
KeyCommandsView = create_objc_class('KeyCommandsView', UIView, [keyCommands, canBecomeFirstResponder, keyCommandAction_])

@on_main_thread
def main():
	main_view = ui.View(frame=(0, 0, 400, 400))
	main_view.name = 'Key Commands Demo'
	
	v = KeyCommandsView.alloc().initWithFrame_(((0, 0), (400, 400)))
	v.setBackgroundColor_(UIColor.lightGrayColor())
	v.becomeFirstResponder()
	ObjCInstance(main_view).addSubview_(v)
	
	label = ui.Label(frame=(0, 0, 400, 400))
	label.alignment = ui.ALIGN_CENTER
	label.text = 'Press Cmd+R on an external keyboard to change the background color. Cmd+B makes the background blue.'
	label.number_of_lines = 0
	main_view.add_subview(label)
	
	main_view.present('sheet')
	
if __name__ == '__main__':
	main()
# --------------------

