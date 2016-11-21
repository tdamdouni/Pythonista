#!python2
# coding: utf-8

import ui
from faker import Faker
import clipboard
import console
import editor
import random
import platform

view = None

fake = Faker()
seed = random.randint(0, 9999)

def slider_changed(sender):
	fake.seed(seed)
	value1 = int(sender.superview['slider1'].value * 10) + 1
	value2 = int(sender.superview['slider2'].value * 10) + 1
	textview = sender.superview['textview1']
	paragraphs = []
	for i in xrange(value2):
		p = fake.paragraph(nb_sentences=value1, variable_nb_sentences=True)
		paragraphs.append(p)
	text = '\n\n'.join(paragraphs)
	textview.text = text
	
def copy_action(sender):
	clipboard.set(sender.superview['textview1'].text)
	console.hud_alert('Copied')
	
def insert_action(sender):
	text = sender.superview['textview1'].text
	start, end = editor.get_selection()
	editor.replace_text(start, end, text)
	if not platform.machine().startswith('iPad'):
		view.close()
		
def randomize_action(sender):
	global seed
	seed = random.randint(0, 9999)
	slider_changed(sender)
	
view = ui.load_view('lorem')
view.present('popover')
slider_changed(view['slider1'])

