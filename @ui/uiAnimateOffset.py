# coding: utf-8

# https://forum.omz-software.com/topic/2438/animate-content-offset

# Any tips implementing the ui.animate() function

import ui
w, h = ui.get_screen_size()
sv = ui.ScrollView()
sv.frame = (0,0,w,h)
sv.background_color = 'gray'
sv.content_size = (0, 2000)
y_offset = 1000
sv.present()
sv.content_offset = (0, y_offset) # animate me

# ...
def scroll():
    sv.content_offset = (0, y_offset)
ui.animate(scroll, 0.5)

# ...
from functools import partial
ui.animate(partial(setattr, sv, 'content_offset', (0, y_offset)), 0.1)