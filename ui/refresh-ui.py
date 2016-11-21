# https://forum.omz-software.com/topic/3589/refresh-ui

import ui
import time

# first get a reference to the image you saved in your Python folder
walking_man_image = ui.Image.named('./assests/sprites/image1.BMP')
walking_man_imageview = ui.ImageView(frame=(30, 0, 180, 180))
walking_man_imageview.image = walking_man_image

@ui.in_background

def start_button_touch_up_inside(sender):
	image_counter = 1
	while image_counter <= 10:
		if image_counter == 1:
			walking_man_image = ui.Image.named('./assests/sprites/image1.BMP')
			walking_man_imageview.image = walking_man_image
		elif image_counter == 2:
			walking_man_image = ui.Image.named('./assests/sprites/image2.BMP')
			walking_man_imageview.image = walking_man_image
		elif image_counter == 3:
			walking_man_image = ui.Image.named('./assests/sprites/image3.BMP')
			walking_man_imageview.image = walking_man_image
		elif image_counter == 4:
			walking_man_image = ui.Image.named('./assests/sprites/image4.BMP')
			walking_man_imageview.image = walking_man_image
			
		# now wait for a fraction of second
		time.sleep(0.2)
		
		image_counter = image_counter + 1
		#print(image_counter)
		view.set_needs_display()
		
view = ui.load_view()

# lastly, add the Imageview into the existing view
view.add_subview(walking_man_imageview)

view.present('sheet')

