# Indent/Outdent selected lines

import editor
import console

indent_char = 't'
text = editor.get_text()
selection = editor.get_line_selection()
selected_text = text[selection[0]:selection[1]]

indent = console.alert('indent or outdent?', '', '\<\<', '\>\>') == 2

replacement = ''
for line in selected_text.splitlines():
	if indent:
		replacement += indent_char + line + 'n'
	else:
		replacement += line[line.find(indent_char) + len(indent_char):] + 'n'
		
editor.replace_text(selection[0], selection[1], replacement)
editor.set_selection(selection[0], selection[0] + len(replacement) - 1)

