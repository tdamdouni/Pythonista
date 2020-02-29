# coding: utf-8

# https://forum.omz-software.com/topic/2570/understanding-ui-redraw-animation

from __future__ import print_function
import ui

def colorIt(lbl):
	lbl.background_color='#ff0000'
	
def buttonClick(sender):
	for item in llst:
		print(item)
		ui.delay(colorIt(item),1.0)
		
v = ui.load_view()

lbl1=v['label1']
lbl2=v['label2']
lbl3=v['label3']
llst=[lbl1,lbl2,lbl3]

v.present('sheet')

#==============================

import ui
from functools import partial

def colorIt(lbl):
	lbl.background_color='#ff0000'
	
def buttonClick(sender):
	for i, item in enumerate(llst):
		print(item)
		ui.delay(partial(colorIt, item), 1.0 * (i+1))
		
v = ui.load_view()

lbl1=v['label1']
lbl2=v['label2']
lbl3=v['label3']
llst=[lbl1,lbl2,lbl3]

v.present('sheet')

