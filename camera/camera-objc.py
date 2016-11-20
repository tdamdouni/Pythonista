# https://forum.omz-software.com/topic/3365/photos-module-start-camera-from-button/22

import ui
import console
import clipboard
from objc_util import *
import photos

SUIViewController = ObjCClass('SUIViewController')

class Extracter(ui.View):
	def __init__(self):
	
		# Some UI Elements
		#(...)
		
		# Take Photo Button
		self.take_photo = ui.Button(flex = 'LR', title = 'Take Photo')
		self.take_photo.action = self.take_photo_action
		# Some Button Styles
		#(...)
		self.add_subview(self.take_photo)
		
	# Take Photo Action
	@ui.in_background
	def take_photo_action(self, sender):
	
		# Show camera
		picker = ObjCClass('UIImagePickerController').alloc().init()
		picker.mame = 'picker'
		picker.delegate = self
		picker.allowsEditing = False
		picker.sourceType = 1 # UIImagePickerControllerSourceTypeCamera
		super_view = sender.superview
		super_view_pntr = ObjCInstance(super_view)
		vc = SUIViewController.viewControllerForView_(super_view_pntr)
		vc.presentModalViewController_animated_(picker, True)
		
		# To get the captured photo, we need to work with delegates
		# not yet developped
		
		
if __name__=='__main__':
	view = Extracter()
	view.present('sheet')

