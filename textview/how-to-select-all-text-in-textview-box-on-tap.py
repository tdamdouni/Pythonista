# coding: utf-8

# https://forum.omz-software.com/topic/2599/how-to-select-all-text-in-text-box-on-tap

# @omz

import ui
from functools import partial

class MyTextViewDelegate (object):
	def textview_did_begin_editing(self, textview):
		r = (0, len(textview.text))
		ui.delay(partial(setattr, textview, 'selected_range', r), 0)
		
tv = ui.TextView(frame=(0, 0, 500, 500))
tv.text = 'Lorem Ipsum Dolor Sit'
tv.font = ('Helvetica', 18)
tv.delegate = MyTextViewDelegate()

tv.present('sheet')

#==============================

import ui
from functools import partial

class golfApp(ui.View):
	...
	def textfield_did_begin_editing(self, textfield):
		r = (0, len(textfield.text))
		ui.delay(partial(setattr, textfield, 'selected_range', r), 0)
	...
	
v=ui.load_view('golf')
v.delegate = MyTextFieldDelegate()
v.present(style='full_screen', orientations='portrait')

#==============================

# @omz

import ui
from objc_util import *
from functools import partial

def select_all(textfield):
	tf = ObjCInstance(textfield).subviews()[0]
	start_pos = tf.beginningOfDocument()
	end_pos = tf.endOfDocument()
	range = tf.textRangeFromPosition_toPosition_(start_pos, end_pos)
	tf.setSelectedTextRange_(range)
	
class MyTextFieldDelegate (object):
	def textfield_did_begin_editing(self, textfield):
		ui.delay(partial(select_all, textfield), 0)
		
tf = ui.TextField(frame=(0, 0, 500, 500))
tf.text = 'Lorem Ipsum Dolor Sit'
tf.font = ('Helvetica', 18)
tf.delegate = MyTextFieldDelegate()
tf.present('sheet')

