from __future__ import print_function
# https://forum.omz-software.com/topic/2254/share-code-progressview
# https://gist.github.com/blmacbeth/60bacd65c89e5290f452

# coding: utf-8

from objc_util import *

## this is bad python styling, but I justify it by saying the
## function is an alias for the UIColor class
def UIColor(red=1.0, green=1.0, blue=1.0, alpha=1.0):
	UIColor = ObjCClass('UIColor')
	r = CGFloat(red)
	g = CGFloat(green)
	b = CGFloat(blue)
	a = CGFloat(alpha)
	return UIColor.colorWithRed_green_blue_alpha_(r,g,b,a)

## same goes for this function. 	
def UIImage(image_string):
	from scene import get_image_path
	UIImage = ObjCClass('UIImage')
	img = UIImage.imageWithContentsOfFile_(get_image_path(image_string))
	return img

## Just convenience class for progress view styles		
class ProgressViewStyle:
	DEFAULT = 0
	BAR     = 1
		
class ProgressView(ui.View):
	@on_main_thread
	def __init__(self, animated=True, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		objc_view = ObjCInstance(self._objc_ptr)
		UIProgressView = ObjCClass('UIProgressView')
		f = CGRect(CGPoint(0, 0), CGSize(self.width, self.height))
		progress_view = UIProgressView.alloc().initWithProgressViewStyle_(0)
		progress_view.setFrame_(f)
		progress_view.setBackgroundColor_(UIColor(*self.background_color))
		flex_width, flex_height = (1<<1), (1<<4)
		progress_view.setAutoresizingMask_(flex_width|flex_height)
		progress_view.autorelease()
		objc_view.addSubview_(progress_view)
		self.progress_view = progress_view
		self.animated = animated
	
	@property
	@on_main_thread
	def progress(self):
		progress_view = self.progress_view
		progress = progress_view.progress()
		return progress
		
	@progress.setter
	@on_main_thread
	def progress(self,progress):
		progress_view = self.progress_view
		progress_view.setProgress_animated_(c_float(progress), self.animated)
	
	@property
	@on_main_thread
	def progress_tint_color(self):
		progress_view = self.progress_view
		color = progress_view.progressTintColor()
		return color
		
	@progress_tint_color.setter
	@on_main_thread
	def progress_tint_color(self, color):
		progress_view = self.progress_view
		progress_view.setProgressTintColor_(UIColor(*color))
	
	@property
	@on_main_thread
	def progress_image(self):
		progress_view = self.progress_view
		image = progress_view.progressImage()
		return image
		
	@progress_image.setter
	@on_main_thread
	def progress_image(self, image_string):
		progress_view = self.progress_view
		progress_view.setProgressImage_(UIImage(image_string))
		
	@property
	@on_main_thread
	def track_tint_color(self):
		progress_view = self.progress_view
		color = progress_view.trackTintColor()
		return color
		
	@track_tint_color.setter
	@on_main_thread
	def track_tint_color(self, color):
		progress_view = self.progress_view
		progress_view.setTrackTintColor_(UIColor(*color))
	
	@property
	@on_main_thread	
	def progress_view_style(self):
		progress_view = self.progress_view
		return progress_view.progressViewStyle()
		
	@progress_view_style.setter
	@on_main_thread
	def progress_view_style(self, style):
		progress_view = self.progress_view
		progress_view.setProgressViewStyle_(style)

def main():
	import time
	progress_view = ProgressView(frame=(0,0,300,50))
	progress_view.name = 'Progress View Example'
	progress_view.track_tint_color = (1.,0,0)
	progress_view.progress_tint_color = (0,1.,0)
	progress_view.present('sheet')
	
	progress_view.progress = 0.0
	for i in range(101):
		progress_view.progress = i/100.
	
	print('Track Color:',    progress_view.track_tint_color)
	print('Progress Color:', progress_view.progress_tint_color)
	
	## commented out because I don't like the image I used and changing
	## the style didn't seem to do anything
	#progress_view.progress_image = 'test:Lenna'
	#progress_view.progress_view_style = ProgressViewStyle.BAR
	progress_view.progress = 0.0
	for i in range(101):
		progress_view.progress = i/100.
	
	print('Progress Image:', progress_view.progress_image)
	print('Animated:',       progress_view.animated)
	
	
if __name__ == '__main__':
	## Uncomment to show what other function are available
	#UIProgressView = ObjCClass('UIProgressView')
	#print dir(UIProgressView.alloc())
	main()