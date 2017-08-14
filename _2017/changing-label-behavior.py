# https://forum.omz-software.com/topic/4183/how-to-add-a-new-line-in-a-button-title/3

import objc_util
import ui

NSLineBreakByWordWrapping = 0
NSLineBreakByCharWrapping = 1
NSLineBreakByClipping = 2
NSLineBreakByTruncatingHead = 3
NSLineBreakByTruncatingTail = 4
NSLineBreakByTruncatingMiddle = 5 # Default for button labels.

b = ui.Button() # Your button (doesn't need to be created here, can come from somewhere else, like a UI file).
objc_util.ObjCInstance(b).button().titleLabel().setLineBreakMode(NSLineBreakByWordWrapping) # You can use any of the line break modes listed above.
