# coding: utf-8

# https://forum.omz-software.com/topic/2268/view-transform-origin

# ui.Transform playground
# discover that all transforms are absolute and override existing transform, unless using concat
# also, discover use for invert, such as changing order of transforms

import ui
from math import pi

v=ui.View(frame=(0,0,700,700),bg_color='white')
target=ui.Label(bg_color=(.5,.5,.5))
target.text='Target'
target.center=500,200
crosshair=ui.Label()
crosshair.text='+'
crosshair.size_to_fit()
crosshair.center=500,200
v.add_subview(target)
v.add_subview(crosshair)

#define some actions which operate on target
def translate_absolute(sender):
   target.transform=ui.Transform.translation(100,0)
def translate_relative(sender):
   target.transform=target.transform.concat(ui.Transform.translation(100,0))
def rotation_relative(sender):
   target.transform=target.transform.concat(ui.Transform.rotation(pi/8.))
def rotation_absolute(sender):
   target.transform=ui.Transform.rotation(pi/8.)
def rotation_relative_in_place(sender):
   # invert current transform, rotate, then redo transform
   inverted_then_rotation_then_transform= target.transform.invert().concat(
         ui.Transform.rotation(pi/8.)).concat(
         target.transform)
   target.transform=target.transform.concat(inverted_then_rotation_then_transform)
def rotate_about_top_r_corner(sender):
   #first, we shift by -w/2,-h/2 to get tr corner at rot center
   # then rotate
   # then shift back so corner matches
   # then spply existing transform
   t=ui.Transform.translation(-target.width/2.,target.height/2.)
   r=ui.Transform.rotation(pi/8.)
   target.transform=t.concat(r).concat(t.invert()).concat(target.transform)
   
   
# build the buttons
buttons=[translate_absolute,
   translate_relative,
   rotation_absolute, 
   rotation_relative, 
   rotation_relative_in_place,
   rotate_about_top_r_corner]

y=400
for b in buttons:
   btn=ui.Button(title=b.__name__)
   btn.action=b
   btn.y=y
   btn.x=50
   btn.height=30
   btn.border_width=1
   btn.bg_color=(1,.7,.7)
   y+=45
   v.add_subview(btn)
v.present()