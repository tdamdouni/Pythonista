# coding: utf-8

# https://github.com/jsbain/objc_hacks/blob/master/attribtxt.py

# experiments with attributed strings

from objc import *
import ctypes

NSMutableAttributedString=ObjCClass('NSMutableAttributedString')
NSFontAttributeName=ns('NSFont')
UIFont=ObjCClass('UIFont')

attrtext = NSMutableAttributedString.alloc()
strtext='This is a ui.Label with attributed strings!'
attrtext.initWithString_(ns(strtext))

sz=6.0
traits=0
for i in xrange(len(strtext)/2):
   f=UIFont.systemFontOfSize_traits_(sz,traits)
   nsr=NSRange(i,1)
   attrtext.addAttribute_value_range_(NSFontAttributeName,f,nsr)
   sz+=2.5
   traits+=1
for i in xrange(len(strtext)/2,len(strtext)-1):
   f=UIFont.systemFontOfSize_traits_(sz,traits)
   nsr=NSRange(i,1)
   attrtext.addAttribute_value_range_(NSFontAttributeName,f,nsr)
   sz-=2.5
   traits+=1
import ui
v=ui.View(frame=(0,0,576,576),bg_color=(0.7,)*3)
lbl=ui.Label(bg_color='white')
v.add_subview(lbl)
v.present('sheet')
lblobj=ObjCInstance(lbl._objc_ptr)
lblobj.setAttributedText_(attrtext)
lbl.size_to_fit()
s=v.draw_snapshot()