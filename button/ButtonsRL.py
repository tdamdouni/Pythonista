#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2473/suggestion-ui-left_button_items-and-right-not-be-none-either-a-empty-tuple-or-list-or-a-property-access/2

from __future__ import print_function
import ui

v = ui.View(frame = (0,0,500,500))
btn_l0 = ui.ButtonItem('left0')
btn_r0 = ui.ButtonItem('right0')
v.left_button_items = [btn_l0]
v.right_button_items = [btn_r0]

btns = [ (btn, btn.enabled) for btn in v.left_button_items + 
            v.right_button_items if isinstance(btn , ui.ButtonItem)]
print(btns)
v.present('sheet')
