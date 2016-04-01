# https://gist.github.com/GuyCarver/4143010
# indent selection

import editor

text = editor.get_text()
selection = editor.get_line_selection()
selected_text = text[selection[0]:selection[1]]
replacement = ''
for line in selected_text.splitlines():
	replacement += '\t' + line + '\n'

editor.replace_text(selection[0], selection[1], replacement)
editor.set_selection(selection[0], selection[0] + len(replacement) - 1)