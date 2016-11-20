# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/notification_capture.py

from objc_util import *
import console
from functools import partial
NSNotificationCenter=ObjCClass('NSNotificationCenter')



#logging.basicConfig(filename='log.txt',format='%(levelname)s:%(message)s', level=logging.DEBUG)

class GlobalNotificationObserver(object):
	def __init__(self, excludes=('UI','NS','_UI'))  :
		self.captured={}
		self.center=NSNotificationCenter.defaultCenter()
		self.excludes=excludes
		self._observer=None
		self._blk=None
		
	def _block(self,_cmd,notification):
		try:
			name=str(ObjCInstance(notification).name())
			if name.startswith(self.excludes):
				return
				
			obj=str(ObjCInstance(notification).object())
			userInfo=str(ObjCInstance(notification).userInfo())
			
			self.captured[name]=str(obj)+str(userInfo)
			#console.hud_alert(name)
		except:
			pass
	def start(self):
		if self._observer:
			raise Exception('observer already started')
		self._blk=ObjCBlock(self._block,
		restype=None,
		argtypes=[c_void_p,c_void_p])
		self._observer = \
		self.center.addObserverForName_object_queue_usingBlock_(None,None,None,self._blk)
		retain_global(self)
		import weakref
		def on_die(killed_ref):
			killed_ref.stop()
	def stop(self):
		import objc_util
		if self._observer:
			self.center.removeObserver_(self._observer)
			self._observer=None
		release_global(self)
	def display_notifications(self):
		import pprint
		pprint.pprint(self.captured)
	def reset(self):
		self.stop()
		self.captured={}
if __name__=='__main__':
	g=GlobalNotificationObserver()
	g.start()

