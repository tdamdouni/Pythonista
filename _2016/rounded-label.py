# https://forum.omz-software.com/topic/3810/rounded-corners-on-labels

# https://forum.omz-software.com/topic/3082/ui-label-corner_radius-not-working

from ui import *
import objc_util

v = View()
v.background_color = 'white'

label = Label()
# label = Button()
# label.title = 'this is button'

label.text = 'This is a label'
label.background_color = 'white'
label.text_color = 'blue'
label.corner_radius = 5
label.border_color = 'black'
label.border_width = 1
label.size_to_fit()
label.center = (v.width * 0.5, v.height * 0.5)
label.flex = 'LRTB'

# The delay is likely the result of setting clipsToBounds on a non-main thread. Try something like on_main_thread(lb.setClipsToBounds_)(True).

# ObjCInstance(lbl).clipsToBounds=True


@objc_util.on_main_thread
def set_rounded(label, radius):
	label.corner_radius = radius
	objc_util.ObjCInstance(label).clipsToBounds = True
	
v.add_subview(label)
v.present('sheet')

