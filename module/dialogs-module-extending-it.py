# coding: utf-8

# https://forum.omz-software.com/topic/2462/dialogs-module-extending-it

# Extension of dialogs.form_dialog() that supports simple data validation

from __future__ import print_function
import dialogs
import collections
import ui

class ValidatingFormDialogController (dialogs._FormDialogController):
	def done_action(self, sender):
		if callable(self.validator):
			invalid_keys = self.validator(self.values)
			if invalid_keys:
				for i, (title, fields) in enumerate(self.sections):
					for j, field in enumerate(fields):
						cell = self.cells[i][j]
						if field['key'] in invalid_keys:
							cell.text_label.text_color = 'red'
						else:
							cell.text_label.text_color = None
				return
		if self.shield_view:
			self.dismiss_datepicker(None)
		else:
			ui.end_editing()
			self.was_canceled = False
			self.container_view.close()
			
def form_dialog(title='', fields=None, sections=None, done_button_title='Done', validator=None):
	if not sections and not fields:
		raise ValueError('sections or fields are required')
	if not sections:
		sections = [('', fields)]
	if not isinstance(title, str) and not isinstance(title, unicode):
		raise TypeError('title must be a string')
	for section in sections:
		if not isinstance(section, collections.Sequence):
			raise TypeError('Sections must be sequences (title, fields)')
		if len(section) < 2:
			raise TypeError('Sections must have 2 or 3 items (title, fields[, footer]')
		if not isinstance(section[0], str) and not isinstance(section[0], unicode):
			raise TypeError('Section titles must be strings')
		if not isinstance(section[1], collections.Sequence):
			raise TypeError('Expected a sequence of field dicts')
		for field in section[1]:
			if not isinstance(field, dict):
				raise TypeError('fields must be dicts')
	c = ValidatingFormDialogController(title, sections, done_button_title=done_button_title)
	c.validator = validator
	c.container_view.present('sheet')
	c.container_view.wait_modal()
	c.container_view = None
	if c.was_canceled:
		return None
	return c.values
	
# --- DEMO:

def validate_form(values):
	# This gets called before the dialog is dismissed via 'Done'.
	# It should return a list of keys that failed to pass validation.
	# If no invalid keys are returned, the dialog is closed as usual,
	# otherwise, the invalid fields are highlighted in red.
	invalid = []
	# Title must be 'Mr', 'Mrs', or 'Ms':
	if values.get('title') not in ['Mr', 'Mrs', 'Ms']:
		invalid.append('title')
	# Name must not be empty:
	if len(values.get('name')) < 1:
		invalid.append('name')
	# 'Accept Terms' must be checked:
	if not values.get('terms'):
		invalid.append('terms')
	return invalid
	
def main():
	fields = [{'type': 'text', 'key': 'title', 'title': 'Title (Mr/Mrs/Ms)'}, {'type': 'text', 'key': 'name', 'title': 'Name'}, {'type': 'switch', 'key': 'terms', 'title': 'Accept Terms'}]
	r = form_dialog('Test', fields, validator=validate_form)
	print(r)
	
if __name__ == '__main__':
	main()
	
#==============================

# coding: utf-8

# Extension of dialogs.form_dialog() that supports simple data validation

import dialogs
import collections
import ui

class ValidatingFormDialogController (dialogs._FormDialogController):
	def done_action(self, sender):
		if callable(self.validator):
			invalid_keys = self.validator(self.values)
			if invalid_keys:
				for i, (title, fields) in enumerate(self.sections):
					for j, field in enumerate(fields):
						cell = self.cells[i][j]
						if field['key'] in invalid_keys:
							cell.text_label.text_color = 'red'
						else:
							cell.text_label.text_color = None
				return
		if self.shield_view:
			self.dismiss_datepicker(None)
		else:
			ui.end_editing()
			self.was_canceled = False
			self.container_view.close()
			
class MyTextFieldDelegate (object):
	def textfield_should_begin_editing(self, textfield):
		return True
	def textfield_did_begin_editing(self, textfield):
		pass
	def textfield_did_end_editing(self, textfield):
		pass
	def textfield_should_return(self, textfield):
		textfield.end_editing()
		return True
	def textfield_should_change(self, textfield, range, replacement):
		if replacement == ' ':
			return False
		print(textfield, range, replacement)
		return True
	def textfield_did_change(self, textfield):
		pass
		
		
def form_dialog(title='', fields=None, sections=None, done_button_title='Done', validator=None):
	if not sections and not fields:
		raise ValueError('sections or fields are required')
	if not sections:
		sections = [('', fields)]
	if not isinstance(title, str) and not isinstance(title, unicode):
		raise TypeError('title must be a string')
	for section in sections:
		if not isinstance(section, collections.Sequence):
			raise TypeError('Sections must be sequences (title, fields)')
		if len(section) < 2:
			raise TypeError('Sections must have 2 or 3 items (title, fields[, footer]')
		if not isinstance(section[0], str) and not isinstance(section[0], unicode):
			raise TypeError('Section titles must be strings')
		if not isinstance(section[1], collections.Sequence):
			raise TypeError('Expected a sequence of field dicts')
		for field in section[1]:
			if not isinstance(field, dict):
				raise TypeError('fields must be dicts')
	c = ValidatingFormDialogController(title, sections, done_button_title=done_button_title)
	cell = c.cells[0][0]
	print(c.cells[0][0].text_label.text)
	tf = cell.content_view.subviews[0]
	tf.text = 'Hi there'
	tf.clear_button_mode = 'when_editing'
	tf.delegate = MyTextFieldDelegate()
	c.validator = validator
	c.container_view.present('sheet')
	c.container_view.wait_modal()
	c.container_view = None
	if c.was_canceled:
		return None
	return c.values
	
# --- DEMO:

def validate_form(values):
	# This gets called before the dialog is dismissed via 'Done'.
	# It should return a list of keys that failed to pass validation.
	# If no invalid keys are returned, the dialog is closed as usual,
	# otherwise, the invalid fields are highlighted in red.
	invalid = []
	# Title must be 'Mr', 'Mrs', or 'Ms':
	if values.get('title') not in ['Mr', 'Mrs', 'Ms']:
		invalid.append('title')
	# Name must not be empty:
	if len(values.get('name')) < 1:
		invalid.append('name')
	# 'Accept Terms' must be checked:
	if not values.get('terms'):
		invalid.append('terms')
	return invalid
	
def main():
	fields = [{'type': 'text', 'key': 'title', 'title': 'Title (Mr/Mrs/Ms)'}, {'type': 'text', 'key': 'name', 'title': 'Name'}, {'type': 'switch', 'key': 'terms', 'title': 'Accept Terms'}]
	r = form_dialog('Test', fields, validator=validate_form)
	print(r)
	
if __name__ == '__main__':
	main()

