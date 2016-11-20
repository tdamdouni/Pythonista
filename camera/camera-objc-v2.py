# https://forum.omz-software.com/topic/3365/photos-module-start-camera-from-button/23

import ui
import console
import clipboard
from objc_util import *


def imagePickerController_didFinishPickingMediaWithInfo_(self,cmd,picker,info):

	pick = ObjCInstance(picker)
	# Set delegate to nil, and release its memory:
	pick.setDelegate_(None)
	ObjCInstance(self).release()
	# Dismiss the sheet:
	pick.dismissViewControllerAnimated_completion_(True, None)
	
	infos = ObjCInstance(info)
	print(infos)
	img = infos['UIImagePickerControllerEditedImage']   # UIImage
	#img = infos['UIImagePickerControllerOriginalImage']
	print(img)
	
	#img.show()
	#photos.save_image(img)
	
SUIViewController = ObjCClass('SUIViewController')

MyPickerDelegate = create_objc_class('MyPickerDelegate',
methods=[imagePickerController_didFinishPickingMediaWithInfo_], protocols=['UIImagePickerControllerDelegate'])

class Extracter(ui.View):
	def __init__(self):
	
		# Take Photo Button
		self.take_photo = ui.Button(flex = 'LR', title = 'Take Photo')
		self.take_photo.action = self.take_photo_action
		self.add_subview(self.take_photo)
		
	# Take Photo Action
	#@ui.in_background
	@on_main_thread
	def take_photo_action(self, sender):
	
		# Show camera
		picker = ObjCClass('UIImagePickerController').alloc().init()
		
		delegate = MyPickerDelegate.alloc().init()
		picker.setDelegate_(delegate)
		
		picker.allowsEditing = True
		picker.sourceType = 1 # UIImagePickerControllerSourceTypeCamera
		super_view = sender.superview
		super_view_pntr = ObjCInstance(super_view)
		vc = SUIViewController.viewControllerForView_(super_view_pntr)
		vc.presentModalViewController_animated_(picker, True)
		
# Protect against import
if __name__ == '__main__':
	view = Extracter()
	view.present('sheet')

