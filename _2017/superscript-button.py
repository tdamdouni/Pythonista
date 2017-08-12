# https://forum.omz-software.com/topic/4223/superscript-text-in-ui-button/9

def superscript(view, itemName, text, size, offset, startPos, length):
	#Get the UI object by name from the current UI view
	target_ui_item = view[itemName]
	#Create a obj-c Mutable Attributed String object and initialize with text
	NSMutableAttributedString = ObjCClass('NSMutableAttributedString')
	attributed_string = NSMutableAttributedString.alloc().initWithString_(ns(text))
	range = NSRange(startPos, length)
	#Create an obj-c Font
	UIFont = ObjCClass('UIFont')
	#Define a List (?) of attributes
	attributes = {
	ns('NSFont'): UIFont.systemFontOfSize(size),
	ns('NSBaselineOffset'): ns(offset)
	}
	#Set the specific attributes of a specific range of the NS Mutable Attributed String
	attributed_string.setAttributes_range_(attributes, range)
	#
	ui_item_objc = ObjCInstance(target_ui_item)
	UIButton = ObjCClass('UIButton')
	for subview in ui_item_objc.subviews():
		if subview.isKindOfClass(UIButton):
			subview.setAttributedTitle_forState_(attributed_string, 0)
			
# superscript(self, 'x_squared', 'x2', 16, 8, 1, 1)
# superscript(self, 'log_base_ten', 'log10', 16, -10, 3, 2)

