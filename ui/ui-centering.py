# https://forum.omz-software.com/topic/3632/ui-centering

import ui

v = ui.View()


v.present('full_screen')
button = ui.Button (title='button')
v.add_subview(button)

button.background_color = 'white'
#button.center =(100,100)
button.width= 360
button.height=100
button.center=(100,100)

