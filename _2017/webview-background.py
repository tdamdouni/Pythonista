# https://forum.omz-software.com/topic/4331/webview-with-transparent-background/3

import ui
from objc_util import ObjCInstance, ObjCClass, on_main_thread

UIWebView = ObjCClass('UIWebView')


def _find_real_webview(view_objc):
	# Traverse subviews and find one which is UIWebView (ObjC)
	for subview_objc in view_objc.subviews():
		if subview_objc.isKindOfClass_(UIWebView.ptr):
			return subview_objc
		else:
			return _find_real_webview(subview_objc)
	return None
	
	
@on_main_thread
def _make_webview_transparent(webview):
	#
	# Any UI manipulation in ObjC must be done on the main thread, thus there's
	# @on_main_thread decorator to ensure that this function is always called
	# on the main thread.
	#
	# Pythonista usually wraps ObjC views / controls / ... in own
	# view. ui.WebView is not real UIWebView, it's kind of wrapper.
	# So we have to get ObjC instance of the wrapper view, traverse
	# subviews and check classes to find real UIWebView (ObjC).
	#
	# Actually ui.WebView (Python) consists of:
	#
	# SUIWebView_PY3 (ObjC)
	#    | UIWebView (ObjC)
	#    |     | _UIWebViewScrollView (ObjC)
	#    |     |     | UIWebBrowserView (ObjC)
	# ...
	#
	pythonista_wrapper_objc = ObjCInstance(webview)
	real_webview_objc = _find_real_webview(pythonista_wrapper_objc)
	if real_webview_objc:
		# UIWebView found
		
		# Make it transparent
		# https://developer.apple.com/documentation/uikit/uiview/1622622-opaque?language=objc
		real_webview_objc.setOpaque_(False)
		
		# Set background color to clear color
		# https://developer.apple.com/documentation/uikit/uicolor/1621945-clearcolor?language=objc
		clear_color = ObjCClass('UIColor').clearColor()
		real_webview_objc.setBackgroundColor_(clear_color)
		
		
class MyView(ui.View):
	def __init__(self):
		self.width = 540
		self.height = 540
		
		# Set background of our main view to yellow color
		self.background_color = '#ffff00'
		
		# Add WebView ...
		self.wv = ui.WebView()
		self.wv.flex = 'WH'
		self.wv.frame = self.bounds
		self.wv.background_color = None  # ... without background color = transparent
		self.add_subview(self.wv)
		
		# Load HTML with transparent background
		self.wv.load_html('<body style="background-color: transparent;">Hallo</body>')
		
		# Since we can't subclass ui.WebView, we made function to make it transparent
		_make_webview_transparent(self.wv)
		
		
def main():
	v = MyView()
	v.present('sheet')
	
	
if __name__ == '__main__':
	main()

