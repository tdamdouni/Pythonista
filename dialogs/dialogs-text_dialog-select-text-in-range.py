# coding: utf-8

# https://forum.omz-software.com/topic/3112/dialogs-text_dialog-select-text-in-range

import ui
import os
from dialogs import _TextDialogController

def my_text_dialog(title='', text='', font=('<system>', 16), autocorrection=None, autocapitalization=ui.AUTOCAPITALIZE_SENTENCES, spellchecking=None, done_button_title='Done', selected_range=None):
	c = _TextDialogController(title=title, text=text, font=font, autocorrection=autocorrection, autocapitalization=autocapitalization, spellchecking=spellchecking, done_button_title=done_button_title)
	if selected_range is not None:
		c.view.selected_range = selected_range
	c.view.present('sheet')
	c.view.begin_editing()
	c.view.wait_modal()
	return c.text
	
filename = 'myfile.txt'
base_name, extension = os.path.splitext(filename)
my_text_dialog('Test', filename, selected_range=(0, len(base_name)))

