#!/usr/bin/env python2

# -*- coding: utf-8 -*-

# https://forum.omz-software.com/topic/3698/how-to-save-user-input-from-text-field-and-use-throughout-script-with-ui/3

""" Random Math View """
from __future__ import print_function


import ui
import random


def eval_answer(sender):
	sender.superview["text_view"].text = sender.text
	
	return sender.text
	
def the_views(s_t):

	""" the view """
	
	try:
	
		#d = U+00F7
		
		count = 0
		
		me_font_20 = "Baskerville-BoldItalic", 20
		
		me_font_30 = "Baskerville-BoldItalic", 30
		
		me_font_80 = "Baskerville-BoldItalic", 80
		
		my_views = ui.View()
		
		my_views.name = "Rand Math"
		
		my_views.border_width = 3
		
		my_views.border_color = "maroon"
		my_views.background_color = "tan"
		
		# Label A random math app
		
		a_label = ui.Label()
		
		a_label.border_width = 3
		
		a_label.border_color = "tan"
		
		a_label.background_color = "maroon"
		
		a_label.frame = (0,0,325,50)
		
		a_label.text = "Random Math App."
		
		a_label.alignment = 50
		
		a_label.font = me_font_30
		
		# Label S how many equations to do
		
		s_label = ui.TextField()
		
		s_label.border_width = 3
		
		s_label.border_color = "maroon"
		
		s_label.background_color = "white"
		
		s_label.frame = (0, 45, 325, 50)
		
		s_label.text = "How many equations: "
		
		s_label.alignment = 50
		
		s_label.font = me_font_20
		
		# Label B top set of numbers
		
		b_label_rand = random.randint(0, 5)
		
		str_b = str(b_label_rand)
		
		b_label = ui.Label()
		
		#b_label.border_width = 3
		
		#b_label.border_color = "tan"
		
		b_label.frame = (80, 150, 180, 90)
		
		b_label.alignment = 50
		
		b_label.font = me_font_80
		
		b_label.text = str_b
		
		# Label C bottom set of numbers
		
		c_label_rand = random.randint(0, 5)
		
		str_c = str(c_label_rand)
		
		while b_label_rand < c_label_rand:
		
			b_label_rand = b_label_rand + c_label_rand
			
		c_label = ui.Label()
		
		#c_label.border_width = 3
		
		#c_label.border_color = "tan"
		
		c_label.frame = (80, 235, 180, 90)
		
		c_label.alignment = 50
		
		c_label.font = me_font_80
		
		c_label.text = str_c
		
		# Label O math operator
		
		o_label_rand = random.choice(["+", "-", "x", "/"])
		
		str_o = str(o_label_rand)
		
		o_label = ui.Label()
		
		#o_label.border_width = 3
		
		#o_label.border_color = "tan"
		
		o_label.frame = (0, 235, 80, 90)
		
		o_label.alignment = 50
		
		o_label.font = me_font_80
		
		o_label.text = str_o
		
		# Label L underline
		
		l_label = ui.Label()
		
		#l_label.border_width = 3
		
		#l_label.border_color = "tan"
		
		l_label.frame = (0, 260, 319, 90)
		
		l_label.alignment = 50
		
		l_label.font = me_font_80
		
		l_label.text = "______"
		
		# TextField answer input
		
		ans_text_field = ui.TextField()
		
		ans_text_field.frame = (75, 340, 185, 90)
		ans_text_field.border_width = 3
		ans_text_field.border_color = "maroon"
		
		ans_text_field.font = me_font_80
		ans_text_field.placeholder = "###"
		
		
		# just to check
		
		ans_text_field.action = eval_answer
		
		text_view = ui.TextView()
		
		text_view.name = "text_view"
		
		text_view.editable = False
		
		text_view.frame = (0, 100, 90, 90)
		my_views.add_subview(text_view)
		
		if eval_answer == 0:
		
			my_views.background_color = "red"
			
		# added subviews
		my_views.add_subview(a_label)
		my_views.add_subview(s_label)
		my_views.add_subview(b_label)
		my_views.add_subview(c_label)
		my_views.add_subview(o_label)
		my_views.add_subview(l_label)
		my_views.add_subview(ans_text_field)
		
		# present sheet
		my_views.present("sheet")
		
	except:
	
		print("failed to load")
		
		
def main():

	""" run the view """
	
	se_te = eval_answer
	
	the_views(se_te)
	
if __name__ == "__main__":
	main()

