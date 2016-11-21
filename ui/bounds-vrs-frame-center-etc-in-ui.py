# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2490/bounds-vrs-frame-center-etc-in-ui/14_

import ui

class Tester(ui.View):
	def __init__(self, frame):
		self.frame = frame
		self.background_color = 'white'
		btn = ui.Button(title = 'test button')
		btn.width = 100
		btn.center = self.center
		self.add_subview(btn)
		
if __name__ == '__main__':
	f = (0,0,500,500)
	t = Tester(frame = f)
	t.present('sheet')
	
###==============================

	btn.center = (self.bounds.center())
	
###==============================

import ui
button = ui.Button(title='button')
button.present(hide_title_bar=True)
print('center', button.center)
print('bounds', button.bounds, button.bounds.center())
print(' frame', button.frame, button.frame.center())

###==============================

# hide_title_bar=False
('center', Point(512.00, 416.00))
('bounds', Rect(0.00, 0.00, 1024.00, 704.00), Point(512.00, 352.00))
(' frame', Rect(0.00, 64.00, 1024.00, 704.00), Point(512.00, 416.00))

# hide_title_bar=True
('center', Point(512.00, 384.00))
('bounds', Rect(0.00, 0.00, 1024.00, 768.00), Point(512.00, 384.00))
(' frame', Rect(0.00, 0.00, 1024.00, 768.00), Point(512.00, 384.00))

###==============================

def layout(self):
		# This will be called when a view is resized. You should typically set the
		# frames of the view's subviews here, if your layout requirements cannot
		# be fulfilled with the standard auto-resizing (flex) attribute.
	pass
	
# ________

import objc_util

def get_presented_size(mode,hide_title_bar=False):
	''' see https://forum.omz-software.com/topic/1618/any-ios-device/7'''
	f=objc_util.ObjCClass('UIApplication').sharedApplication().keyWindow().frame()
	sz= ui.Size(f.size.width,f.size.height)
	if sz[1]<=320:
		status_height=0
		title_height=32
	else:
		status_height=20
		title_height=44
		
	if mode=='sheet':
		maxsize=min( sz-(0,title_height*(not hide_title_bar)))
		return ui.Size(maxsize,maxsize)
	elif mode=='panel':
		return sz-(0,status_height+(title_height*(not hide_title_bar)))
	elif mode=='fullscreen':
		return sz-(0,(title_height*(not hide_title_bar)))

