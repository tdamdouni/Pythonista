# ColorMixer
# A simple RGB color mixer with three sliders.

import ui
from console import hud_alert
import webbrowser
import sys
import os
import urllib

icon = 'Spanner'
if len(sys.argv) > 1:
	icon = sys.argv[1]

topcolor = []
bottomcolor = []

def slidercolor():
	r = v['slider1'].value
	g = v['slider2'].value
	b = v['slider3'].value
	return [int(i*255) for i in (r,g,b)]

def ok_tapped(sender):
	global topcolor
	global bottomcolor
	if len(topcolor) != 0:
		bottomcolor = slidercolor()
		quit()
	else:
		topcolor = slidercolor()
		v.name = 'Bottom Color'

def quit():
	v.close()
	tcs = ','.join(str(i) for i in topcolor)
	bcs = ','.join(str(i) for i in bottomcolor)
	fpath = sys.argv[0].split('/Documents/',1)[1]
	dpath = os.path.dirname(fpath)
	webbrowser.open('pythonista://' + urllib.quote(dpath+'/create.py') + '?action=run&argv='+urllib.quote(tcs) + '&argv='+urllib.quote(bcs) + '&argv='+urllib.quote(icon))
	
	
	
def makegray_tapped(sender):
	v['slider1'].value = v['slider2'].value = v['slider3'].value = v['slider1'].value
	slider_action(v['slider1'])

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
	
v = ui.load_view('choosecolor')
slider_action(v['slider1'])
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('popover')
else:
	# iPhone
	v.present()

