# Comment/Uncomment selected lines

import editor

text = editor.get_text()
selection = editor.get_line_selection()
selected_text = text[selection[0]:selection[1]]
is_comment = selected_text.strip().startswith('#')
replacement = ''
for line in selected_text.splitlines():
	if is_comment:
		if line.strip().startswith('# '):
			replacement += line[line.find('# ') + 2:] + '\n'
		elif line.strip().startswith('#'):
			replacement += line[line.find('#') + 1:] + '\n'
		else:
			replacement += line + '\n'
	else:
		replacement += '# ' + line + '\n'

editor.replace_text(selection[0], selection[1], replacement)
editor.set_selection(selection[0], selection[0] + len(replacement) - 1)
