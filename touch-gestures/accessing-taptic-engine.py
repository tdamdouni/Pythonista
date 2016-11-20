from objc_util import *

UIDevice = ObjCClass('UIDevice')

def taptic_peek():
	d = UIDevice.new()
	t = d._tapticEngine()
	t.actuateFeedback_(1001)
	
def taptic_pop():
	d = UIDevice.new()
	t = d._tapticEngine()
	t.actuateFeedback_(1002)

