# coding: utf-8

# https://github.com/HeyItsJono/Pythonista

import math
import ui
import clipboard
import decimal
from console import hud_alert

shows_result = False

def num(s):
	try:
		return int(s)
	except ValueError:
		return decimal.Decimal(s)

def button_tapped(sender):
	'@type sender: ui.Button'
	t = sender.title
	global shows_result
	
	labelmain = sender.superview['labelmain']
	labelbase = sender.superview['labelbase']
	segment = sender.superview['segmentedcontrol']
	
	if segment.selected_index == 0:
		if t in '0123456789':
			if shows_result or labelmain.text == '0':
				labelmain.text = t
				shows_result = False
			else:
				labelmain.text += t
		elif t == '.' and '.' not in labelmain.text:
			labelmain.text += t
		elif t == 'AC':
			labelmain.text = '0'
		elif t == 'C':
			labelmain.text = labelmain.text[:-1]
			if len(labelmain.text) < 1:
				labelmain.text = '0'
		elif t == 'e':
			labelmain.text = str(math.e)
		elif t == '+/-':
			if '-' in labelmain.text:
				labelmain.text = labelmain.text[1:]
			else:
				labelmain.text = '-' + labelmain.text
		elif t == '=':
			try:
				result = str(math.log(num(labelmain.text), num(labelbase.text)))
				labelmain.text = result
			except ValueError:
				try:
					result = str(math.log(num(labelmain.text), 10))
					labelmain.text = result
				except Exception as error:
					labelmain.text = str(error)
					print error
			shows_result = True
		elif t != '=':
			shows_result = False
	else:
		if t in '0123456789':
			if labelbase.text == '0':
				labelbase.text = t
			else:
				labelbase.text += t
		elif t == '.' and '.' not in labelbase.text:
			labelbase.text += t
		elif t == 'AC':
			labelbase.text = '0'
		elif t == 'C':
			labelbase.text = labelbase.text[:-1]
			if len(labelbase.text) < 1:
				labelbase.text = '0'
		elif t == 'e':
			labelbase.text = str(math.e)
		elif t == '+/-':
			if '-' in labelbase.text:
				labelbase.text = labelbase.text[1:]
			else:
				labelbase.text = '-' + labelbase.text
		elif t == '=':
			try:
				result = str(math.log(num(labelmain.text), num(labelbase.text)))
				labelmain.text = result
			except ValueError:
				try:
					result = str(math.log(num(labelmain.text), 10))
					labelmain.text = result
				except Exception as error:
					labelmain.text = str(error)
					print error
			shows_result = True
		elif t != '=':
			shows_result = False

def copy_action(sender):
	'@type sender: ui.Button'
	
	clipboard.set(sender.superview['labelmain'].text)
	hud_alert('Copied')

v = ui.load_view('Log Calculator')
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('sheet')
else:
	# iPhone
	v.present(orientations=['portrait'])