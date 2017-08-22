# https://gist.github.com/omz/b76261844db0255899ba857838a7c201

# Pythonista script to show the UI Debugging overlay (private API) described in this blog post:
# http://ryanipete.com/blog/ios/swift/objective-c/uidebugginginformationoverlay/

from objc_util import ObjCClass, on_main_thread
UIDebuggingInformationOverlay = ObjCClass('UIDebuggingInformationOverlay')

@on_main_thread
def toggle_overlay():
  UIDebuggingInformationOverlay.prepareDebuggingOverlay()
  UIDebuggingInformationOverlay.overlay().toggleVisibility()

toggle_overlay()
