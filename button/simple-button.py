#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2836/just-a-simple-button

# You're almost there. Just move the button_tapped function above the load_view call.

# In your script, button_tapped is not yet defined when load_view is called, so the action can't be bound.

from __future__ import print_function
import ui
import console

v = ui.load_view()
v.present('sheet')

# As a function:
def button_tapped(sender):
	print('button tapped')

