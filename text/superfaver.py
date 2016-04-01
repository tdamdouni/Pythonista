# https://gist.github.com/JoeIsHere/cfb751c7b4f94a4dd90a
# -*- coding: utf-8 -*-
# iOS Pythonista import
import console
import clipboard
console.set_font('Helvetica Neue')
# End Pythonista import

superf = u"""
☆。 ★。 ☆  ★
 。☆ 。☆。☆ 
★。＼｜／。★   
  SUPERFAVE
★。／｜＼。★ 
 。 ☆。☆。☆ 
☆。 ★。 ☆  ★
"""
print()
print(superf)
a = raw_input(u'★  = ')
b = raw_input(u'☆  = ')
r = superf.replace(u'★',a).replace(u'☆',b)
print(r)
#iOS Pythonista
clipboard.set(r)