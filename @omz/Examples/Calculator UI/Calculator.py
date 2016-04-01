# coding: utf-8

# Calculator

from __future__ import division
import ui
import clipboard
from console import hud_alert

shows_result = False

def button_tapped(sender):
	'@type sender: ui.Button'
	# Get the button's title for the following logic:
	t = sender.title
	global shows_result
	# Get the labels:
	label = sender.superview['label1']
	label2 = sender.superview['label2']
	if t in '0123456789':
		if shows_result or label.text == '0':
			# Replace 0 or last result with number:
			label.text = t
		else:
			# Append number:
			label.text += t
	elif t == '.' and label.text[-1] != '.':
		# Append decimal point (if not already there)
		label.text += t
	elif t in '+-÷×':
		if label.text[-1] in '+-÷×':
			# Replace current operator
			label.text = label.text[:-1] + t
		else:
			# Append operator
			label.text += t
	elif t == 'AC':
		# Clear All
		label.text = '0'
	elif t == 'C':
		# Delete the last character:
		label.text = label.text[:-1]
		if len(label.text) == 0:
			label.text = '0'
	elif t == '=':
		# Evaluate the result:
		try:
			label2.text = label.text + ' ='
			expr = label.text.replace('÷', '/').replace('×', '*')
			label.text = str(eval(expr))
		except (SyntaxError, ZeroDivisionError):
			label.text = 'ERROR'
		shows_result = True
	if t != '=':
		shows_result = False
		label2.text = ''

def copy_action(sender):
	'@type sender: ui.Button'
	t1 = sender.superview['label1'].text
	t2 = sender.superview['label2'].text
	if t2:
		text = t2 + ' ' + t1
	else:
		text = t1
	clipboard.set(text)
	hud_alert('Copied')

v = ui.load_view('Calculator')

if min(ui.get_screen_size()) >= 768:
	# iPad
	v.frame = (0, 0, 360, 400)
	v.present('sheet')
else:
	# iPhone
	v.present(orientations=['portrait'])