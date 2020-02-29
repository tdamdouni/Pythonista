from __future__ import print_function
# https://forum.omz-software.com/topic/3734/use-keycommand-in-conjunction-with-superview-and-pyui

from objc_util import *
import ui

UIKeyCommand = ObjCClass('UIKeyCommand')
modifiers = {(1<<17): 'Shift', (1<<18): 'Ctrl', (1<<19): 'Alt', (1<<20): 'Cmd', (1<<21): 'NumPad'}

def keyCommands(_self, _cmd):
	cmd_key_flag = (1<<20)
	key_a = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('A', 0,'keyCommandAction:')
	key_s = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('S', 0, 'keyCommandAction:')
	key_d = UIKeyCommand.keyCommandWithInput_modifierFlags_action_('D', 0, 'keyCommandAction:')
	
	commands = ns([key_a, key_s, key_d])
	return commands.ptr
	
def canBecomeFirstResponder(_self, _cmd):
	return True
	
def keyCommandAction_(_self, _cmd, sender):
	self = ObjCInstance(_self)
	key_cmd = ObjCInstance(sender)
	flags = key_cmd.modifierFlags()
	modifier_str = ' + '.join(modifiers[m] for m in modifiers.keys() if (m & flags))
	key_input = key_cmd.input()
	print('Input: "%s" Modifiers: %s' % (key_input, modifier_str))
	if str(key_input) == 'A':
		A(sender)
	elif str(key_input) == 'S':
		S(sender)
	else:
		D(sender)
		
def A(sender):
	Alabel = sender.superview['Alabel']
	Alabel.text = str('Pusshed-A')
def S(sender):
	print('pusshed-S')
	
def D(sender):
	print('pusshed-D')
	
FCCF = create_objc_class('FCCF', UIView, [keyCommands, canBecomeFirstResponder, keyCommandAction_])
main_view = ui.load_view('FC')
v = FCCF.alloc().initWithFrame_(((0, 0), (1, 1)))
v.becomeFirstResponder()
ObjCInstance(main_view).addSubview_(v)
main_view.present('sheet')
