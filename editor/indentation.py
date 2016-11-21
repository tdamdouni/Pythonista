import editor, console

script = editor.get_text()
selection = editor.get_selection()
selected_text = script[selection[0]:selection[1]].splitlines()
indentation = int(console.input_alert('Indent'))
replacement = []

for line in selected_text:
	if indentation > 0:
		replacement.append(('\t'*indentation)+line+('\n' if line != selected_text[-1] else ''))
	elif indentation == 0:
		replacement.append(line+('\n' if line != selected_text[-1] else ''))
	elif indentation < 0:
		if len(line) == 0:
			replacement.append('\n')
		elif line[0] == '\t':
			indent = min(abs(indentation), line.count('\t'))
			replacement.append(line.replace('\t', '', indent)+('\n' if line != selected_text[-1] else ''))
		else:
			replacement.append(line+('\n' if line != selected_text[-1] else ''))
			
editor.replace_text(selection[0], selection[1], ''.join(replacement))

