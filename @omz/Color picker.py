# https://gist.github.com/omz/ae96874dfbda54ed2771

import ui
from random import randint
import console
import clipboard
# Generate some random hex colors:

colors = ['#%X%X%X' % (randint(0,255), randint(0,255), randint(0,255)) for i in xrange(25)]
def tapped(sender):
	r, g, b, a = sender.background_color
	hex_color = '#%X%X%X' % (int(r*255), int(g*255), int(b*255))
	clipboard.set(hex_color)
	console.hud_alert(hex_color + ' copied')
	
#Add buttons for all the colors to a scroll view:
scroll_view = ui.ScrollView(frame=(0, 0, 400, 400))
scroll_view.content_size = (0, len(colors) * 80)
for i, c in enumerate(colors):
	swatch = ui.Button(frame=(0, i*80, 400, 80), background_color=c)
	swatch.flex = 'w'
	swatch.action = tapped
	scroll_view.add_subview(swatch)
scroll_view.name = 'Random Color Picker'
scroll_view.present('sheet')