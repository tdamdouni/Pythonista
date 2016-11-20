# https://forum.omz-software.com/topic/3365/photos-module-start-camera-from-button

import ui
import console
import clipboard
import photos

class Extracter(ui.View):
	def __init__(self):
	
	# Some UI Elements
	(...)
	
	# Take Photo Button
	self.take_photo = ui.Button(flex = 'LR', title = 'Take Photo')
	self.take_photo.action = self.take_photo_action
	# Some Button Styles
	(...)
	
	# Take Photo Action
	@ui.in_background
	def take_photo_action(self, sender):
		image = photos.capture_image()
		
if __name__=='__main__':
	view = Extracter()

# --------------------

import ui
import console
import clipboard
import photos

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
		image = photos.capture_image()
		photos.save_image(image)
		
if __name__=='__main__':
	view = Extracter()
	view.present('sheet')

# --------------------

   # Take Photo Action
    @ui.in_background
    def take_photo_action(self, sender):
        image = photos.capture_image()
        def a():
           photos.save_image(image)
           self.close()
        ui.delay(a,.5)

# --------------------

import ui
import photos

class Extracter(ui.View):
    def __init__(self):
        print('Executed')
        photos.capture_image()
        
if __name__=='__main__':
    view = Extracter()

# --------------------

import ui
import photos

photos.capture_image()

class Extracter(ui.View):
    def __init__(self):
        print('Executed')
        
if __name__=='__main__':
    view = Extracter()
