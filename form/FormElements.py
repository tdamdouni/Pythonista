from __future__ import print_function
# https://gist.github.com/9e2163e1041a3e17d210

# FormElements
#
# These functions create form elements as HTML strings. Call them
# while constructing HTML strings for form-based applications.
#
# All functions automatically add string.Template placeholders
# (e.g. ${name_value}) inside each element to facilitate replacement
# with run-time data and maintaining form state. Use the .substitute
# or .safe_substitute methods to replace the placeholders.
#
# The textbox and textarea placeholders represent the text that will
# populate the form fields, at startup as well as after a response.
# The select, radio, and checkbox placeholders represent 'selected'
# or 'checked' attributes used to pre-select options and maintain
# state after a response.
#
# The select, radio, and checkbox funtions accept either one or two
# dimensional (nested) lists for the options argument. Nested lists
# are used when the displayed content is different than the value.
#
# All functions include an attrib argument which, for some, defaults
# to an onchange event form submit, but can be used to insert any
# other element attributes such as classes, styles, etc.

from types import *

def create_textbox(name, size = 20, attrib = ''):
	"""create_textbox: creates an HTML text input element"""
	html = ('<input type="text" name="' + name + '" id="' + name + '"' +
	' size="' + str(size) + '" ' + attrib +
	' value="${' + name + '}" />\n')
	return html
	
def create_textarea(name, cols = 20, rows = 4, attrib = ''):
	"""create_textarea: creates an HTML textarea element"""
	html = ('<textarea name="' + name + '" id="' + name + '"' +
	' cols="' + str(cols) + '" rows="' + str(rows) + '"' +
	' ' + attrib + '>${' + name + '}</textarea>\n')
	return html
	
def create_select(name, options, attrib = 'onchange="submit()"'):
	"""create_select: creates an HTML select element"""
	html = '<select name="' + name + '" id="' + name + '" ' + attrib + '>\n'
	if type(options[0]) is ListType:
		for o in options:
			opt = str(o[0])
			val = str(o[1])
			html += ('<option value="' + val + '" ' +
			'${' + name + '_' + val + '}>' + opt + '\n')
	else:
		for o in options:
			val = str(o)
			html += '<option ${' + name + '_' + val + '}>' + val + '\n'
	html += '<select>\n'
	return html
	
def create_radios(name, options, attrib = 'onchange="submit()"'):
	"""create_radios: creates HTML radio input elements"""
	html = ''
	if type(options[0]) is ListType:
		for o in options:
			opt = str(o[0])
			val = str(o[1])
			html += ('<input type="radio" name="' + name + '" ' +
			attrib + ' value="' + val + '" ' +
			'${' + name + '_' + val + '} /> ' + opt + '\n')
	else:
		for o in options:
			val = str(o)
			html += ('<input type="radio" name="' + name + '" ' +
			attrib + ' ${' + name + '_' + val + '} /> ' + val + '\n')
	return html
	
def create_checkboxes(name, options, attrib = 'onchange="submit()"'):
	"""create_checkboxes: creates HTML checkbox input elements"""
	html = ''
	if type(options[0]) is ListType:
		for o in options:
			opt = str(o[0])
			val = str(o[1])
			html += ('<input type="checkbox" name="' + name + '" ' +
			attrib + ' value="' + val + '" ' +
			'${' + name + '_' + val + '} /> ' + opt + '\n')
	else:
		for o in options:
			val = str(o)
			html += ('<input type="checkbox" name="' + name + '" ' +
			attrib + ' ${' + name + '_' + val + '} /> ' + val + '\n')
	return html
	
#test elements
if __name__ == '__main__':
	print(create_textbox('txt', 20))
	print(create_textarea('txtarea', 20, 4))
	#options = [1, 2, 3]
	options = [['one', 1], ['two', 2], ['three', 3]]
	print(create_select('sel', options))
	print(create_radios('rdo', options))
	print(create_checkboxes('chk', options))

