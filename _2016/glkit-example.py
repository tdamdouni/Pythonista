# https://forum.omz-software.com/topic/2066/python-opengles

# @omz

from objc_util import *
import time
import colorsys

GLKView = ObjCClass('GLKView')
GLKViewController = ObjCClass('GLKViewController')
UINavigationController = ObjCClass('UINavigationController')
UIBarButtonItem = ObjCClass('UIBarButtonItem')
EAGLContext = ObjCClass('EAGLContext')

glClearColor = c.glClearColor
glClearColor.restype = None
glClearColor.argtypes = [c_float, c_float, c_float, c_float]
glClear = c.glClear
glClear.restype = None
glClear.argtypes = [c_uint]
GL_COLOR_BUFFER_BIT = 0x00004000

def glkView_drawInRect_(_self, _cmd, view, rect):
	r, g, b = colorsys.hsv_to_rgb((time.time() * 0.1) % 1.0, 1, 1)
	glClearColor(r, g, b, 1.0)
	glClear(GL_COLOR_BUFFER_BIT)
MyGLViewDelegate = create_objc_class('MyGLViewDelegate', methods=[glkView_drawInRect_], protocols=['GLKViewDelegate'])

def dismiss(_self, _cmd):
	self = ObjCInstance(_self)
	self.view().delegate().release()
	self.view().setDelegate_(None)
	self.dismissViewControllerAnimated_completion_(True, None)
MyGLViewController = create_objc_class('MyGLViewController', GLKViewController, methods=[dismiss])

@on_main_thread
def main():
	context = EAGLContext.alloc().initWithAPI_(2).autorelease()
	glview = GLKView.alloc().initWithFrame_(((0, 0), (320, 320))).autorelease()
	delegate = MyGLViewDelegate.alloc().init()
	glview.setDelegate_(delegate)
	glview.setContext_(context)
	glview.setEnableSetNeedsDisplay_(False)
	glvc = MyGLViewController.alloc().initWithNibName_bundle_(None, None).autorelease()
	glvc.setTitle_('GLKit Demo')
	glvc.setView_(glview)
	done_b = UIBarButtonItem.alloc().initWithTitle_style_target_action_('Done', 2, glvc, 'dismiss').autorelease()
	glvc.navigationItem().setRightBarButtonItem_(done_b)
	nav = UINavigationController.alloc().initWithRootViewController_(glvc)
	rootvc = UIApplication.sharedApplication().keyWindow().rootViewController()
	rootvc.presentModalViewController_animated_(nav, True)
	nav.release()
	
main()

