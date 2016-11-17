# coding: utf-8

# https://gist.github.com/bmw1821/83507f246e3b611f9f98 

# Py3

from objc_util import *

def __setup():
	global __show_touches_setup_complete
	try:
		return __show_touches_setup_complete
	except NameError:
		pass
		
	c.method_setImplementation.restype = c_void_p
	c.method_setImplementation.argtypes = [c_void_p, c_void_p]
	
	c.method_getImplementation.restype = c_void_p
	c.method_getImplementation.argtypes = [c_void_p]
	
	app = UIApplication.sharedApplication()
	
	global __tvs
	__tvs = {}
	
	def sendEvent2_(_self, _cmd, _event):
		from objc_util import ObjCInstance, CGRect, ObjCClass
		
		UIView = ObjCClass('UIView')
		
		try:
			self = ObjCInstance(_self)
			e = ObjCInstance(_event)
			self.sendEvent2_(e)
			global __tvs
			global __show_touches
			if not __show_touches:
				if __tvs:
					if len(__tvs) > 0:
						for k, v in enumerate(__tvs):
							v[1].removeFromSuperview()
							__tvs.pop(k)
				return
			for tid in __tvs.keys():
				ids = [id(t) for t in e.allTouches().allObjects()]
				if not tid in ids:
					__tvs[tid][1].removeFromSuperview()
					__tvs.pop(tid)
			for t in e.allTouches().allObjects():
				if t.phase() == 3 or t.phase() == 4:
					__tvs[id(t)][1].removeFromSuperview()
					__tvs.pop(id(t), None)
				elif t.phase() == 0:
					vc = t.window().rootViewController()
					while vc.presentedViewController():
						vc = vc.presentedViewController()
					v = UIView.new()
					v.size = (30, 30)
					v.center = t.locationInView_(vc.view())
					v.backgroundColor = UIColor.blackColor()
					v.alpha = 0.4
					v.layer().cornerRadius = 15
					v.userInteractionEnabled = False
					vc.view().addSubview_(v)
					__tvs[id(t)] = [t, v]
				elif t.phase() == 1:
					__tvs[id(t)][0] = t
					vc = t.window().rootViewController()
					while vc.presentedViewController():
						vc = vc.presentedViewController()
					v = __tvs[id(t)][1]
					v.center = t.locationInView_(vc.view())
		except:
			pass
			
	MyApp = create_objc_class('MyApp', NSObject, methods = [sendEvent2_])
	
	newimp = c.method_getImplementation(MyApp.new().sendEvent2_.method)
	c.class_addMethod(UIApplication.ptr, sel('sendEvent2_'), newimp, c.method_getTypeEncoding(app.sendEvent_.method))
	oldimp = c.method_getImplementation(app.sendEvent_.method)
	
	c.method_setImplementation(app.sendEvent_.method, newimp)
	c.method_setImplementation(app.sendEvent2_.method, oldimp)
	
	__show_touches_setup_complete = True
	
def set_show_touches(show_touches):
	__setup()
	global __show_touches
	__show_touches = show_touches
