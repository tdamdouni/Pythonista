# ColorMixer
# A simple RGB color mixer with three sliders.

import ui
import clipboard
from random import random
from console import hud_alert

def slider_action(sender):
	# Get the root view:
	v = sender.superview
	# Get the sliders:
	r = v['slider1'].value
	g = v['slider2'].value
	b = v['slider3'].value
	# Create the new color from the slider values:
	v['view1'].background_color = (r, g, b)
	v['label1'].text = '#%.02X%.02X%.02X' % (r*255, g*255, b*255)

def copy_action(sender):
	clipboard.set(sender.superview['label1'].text)
	hud_alert('Copied')

def shuffle_action(sender):
	v = sender.superview
	s1 = v['slider1']
	s2 = v['slider2']
	s3 = v['slider3']
	s1.value = random()
	s2.value = random()
	s3.value = random()
	slider_action(s1)

v = ui.load_view('ColorMixer')
slider_action(v['slider1'])
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('popover')
else:
	# iPhone
	v.present()

