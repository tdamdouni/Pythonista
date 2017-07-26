# https://forum.omz-software.com/topic/3810/rounded-corners-on-labels/7

from ui import *

v = View()
v.background_color = 'white'  

label = Label()
label.text = 'this is label'
label.background_color = (1,1,1,0) # transparent background
label.text_color = 'white'
label.corner_radius = 10
label.border_color = 'white'
label.border_width = 1
label.size_to_fit()
label.center = (v.width * 0.5, v.height * 0.5)
label.flex = 'LRTB' 
v.add_subview(label)

label_button = Button()
label_button.frame = label.frame
label_button.background_color = 'black'
label_button.text_color = 'white'
label_button.corner_radius = 10
label_button.border_color = 'white'
label_button.border_width = 1
v.add_subview(label_button)
label_button.send_to_back()

v.present('sheet')
