#!python2
# coding: utf-8

# @OMZ

# https://forum.omz-software.com/topic/2230/selectors-in-python/4

# Here's an example for defining an ObjC class to use as the target for your action:

# coding: utf-8

from __future__ import print_function
from objc_util import *
import ui

UIBarButtonItem = ObjCClass('UIBarButtonItem')
UIBarButtonItemGroup = ObjCClass('UIBarButtonItemGroup')

def btnAction(_self, _cmd):
	print('hello world')
	
ActionTarget = create_objc_class('ActionTarget', methods=[btnAction])
target = ActionTarget.new().autorelease()

@on_main_thread
def main():
	tv = ui.TextView(frame=(0, 0, 320, 320))
	b1 = UIBarButtonItem.alloc().initWithTitle_style_target_action_('H', 0, target, 'btnAction').autorelease()
	group = UIBarButtonItemGroup.alloc().initWithBarButtonItems_representativeItem_([b1], None).autorelease()
	ObjCInstance(tv).inputAssistantItem().trailingBarButtonGroups = [group]
	tv.present('sheet')
	
if __name__ == '__main__':
	main()

