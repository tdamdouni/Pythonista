# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/attrib_textview_typing.py

# experiments with attributed strings

from objc_util import *
import ctypes

NSMutableAttributedString=ObjCClass('NSMutableAttributedString')
UIColor=ObjCClass('UIColor')
NSFontAttributeName=ns('NSFont')
NSForegroundColorAttributeName=ns('NSColor')
UIFont=ObjCClass('UIFont')


import ui



def buildAttributes():
   #   d=NSMutableDictionary.new()
   d={
      NSForegroundColorAttributeName:UIColor.colorWithRed_green_blue_alpha_(tv.R,tv.G,tv.B,1.),
      NSFontAttributeName:UIFont.systemFontOfSize_(tv.fontsize)
}
   tvobj.setTypingAttributes_(d)
   desclbl.text='Font size={} R={:0.2f}, G={:0.2f}, B={:0.2f}'.format(tv.fontsize, tv.R, tv.G, tv.B)
   return d
   
def SizeSliderAction(sender):
   tv.fontsize=round(6+sender.value*72.0)
   buildAttributes()

   
def RGBSliderAction(color):
   def action(sender):
      setattr(tv,color,sender.value)
      buildAttributes()
   return action
count=0
def textview_should_change(sender,text):
   global count
   buildAttributes()
   count+=1
   return True
v=ui.View(frame=(0,0,576,576),bg_color=(0.7,)*3)
txtsize=ui.Slider(bg_color=(1,1,1),frame=(0,50,300,30))
redslider=ui.Slider(bg_color=(1,0,0),frame=(0,80,300,30))
greenslider=ui.Slider(bg_color=(0,1,0),frame=(0,110,300,30))
blueslider=ui.Slider(bg_color=(0,0,1),frame=(0,140,300,30))

txtsize.action=SizeSliderAction
redslider.action=RGBSliderAction('R')
greenslider.action=RGBSliderAction('G')
blueslider.action=RGBSliderAction('B')


desclbl=ui.Label(frame=(0,0,300,20))

v.add_subview(txtsize)
v.add_subview(redslider)
v.add_subview(greenslider)
v.add_subview(blueslider)
v.add_subview(desclbl)
tv=ui.TextView(bg_color='white',frame=(0,150,300,300))

tv.textview_should_change=textview_should_change
tv.delegate=tv
tv.fontsize=12
tv.R=0
tv.G=0
tv.B=0
tv.text='type here'

txtsize.value=(tv.font[1]-6)/72.0
v.add_subview(tv)
v.present('sheet')
tvobj=ObjCInstance(tv)
buildAttributes()