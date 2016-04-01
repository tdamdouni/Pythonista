# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/attribtext2.py

# set attributed text dor existing textview

# same works for Label, except dont need to set allowsAttributedTextEditing, or call on main thread

from objc_util import *

mystr='''here are some colors:
   red, yellow, blue, magenta, black, cyan
this is also editable
'''
mystro=ObjCClass('NSMutableAttributedString').alloc().initWithString_(mystr)

   
UIColor=ObjCClass('UIColor')

colors={'red': UIColor.redColor(),
'green':UIColor.greenColor(),
'blue':UIColor.blueColor(),
'cyan':UIColor.cyanColor(),
'magenta':UIColor.magentaColor(),
'black':UIColor.blackColor(),
'yellow':UIColor.yellowColor()}

# go through each thing i want to highlight, and addAttribute to that range
for k,color in colors.items():
   sre=re.finditer(k,mystr)
   for m in sre:
      st,end=m.span()
      l=end-st
      mystro.addAttribute_value_range_('NSColor',color,NSRange(st,l))

# setup views
import ui

v=ui.View(bg_color='white',frame=(0,0,300,300))
tv=ui.TextView(flex='wh',frame=v.bounds)
v.add_subview(tv)
v.present('sheet')
#set up objc instance
tvo=ObjCInstance(tv)
def setAttribs():
   tvo.setAllowsEditingTextAttributes_(True)
   tvo.setAttributedText_(mystro)
on_main_thread(setAttribs)()      #apparently this must be called on main thread for textview