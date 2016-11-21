# coding: utf-8

# https://forum.omz-software.com/topic/3058/navigationview-does-not-like-being-presented-as-a-panel

import ui

v=ui.View(bg_color='red')
n=ui.NavigationView(v)
n.present('panel')
n.close() # or, closing manually

