# https://forum.omz-software.com/topic/3368/objc-setstatusbarhidden-possible

from objc_hacks import swizzle
from objc_util import ObjCClass, UIApplication
import objc_util # for hideStatusBar storage

try:
	objc_util.hideStatusBar
except AttributeError:
	objc_util.hideStatusBar=False
	
def togglestatusbar():
	objc_util.hideStatusBar=not objc_util.hideStatusBar
	UIApplication.sharedApplication().\
	_rootViewControllers()[0].setNeedsStatusBarAppearanceUpdate()
	
def prefersStatusBarHidden(obj,cmd):
	return objc_util.hideStatusBar
swizzle.swizzle(
    ObjCClass('PASlidingContainerViewController'),
    'prefersStatusBarHidden',
    prefersStatusBarHidden)
UIApplication.sharedApplication().\
            _rootViewControllers()[0].\
            setNeedsStatusBarAppearanceUpdate()

togglestatusbar()

