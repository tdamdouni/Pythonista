# https://forum.omz-software.com/topic/3589/refresh-ui/3

import time, ui

imageview = ui.ImageView(frame=(30, 0, 180, 180))

# a list of ten images
images = [ui.Image.named('plf:Hud{}'.format(i)) for i in range(10)]

def start_button_touch_up_inside(sender):
	for i in range(30):
		imageview.image = images[i % len(images)]
		# now wait for a fraction of second
		time.sleep(0.2)
		# view.set_needs_display()
		
#view = ui.load_view()
view = ui.View()

# lastly, add the Imageview into the existing view
view.add_subview(imageview)

view.present()
start_button_touch_up_inside(None)

