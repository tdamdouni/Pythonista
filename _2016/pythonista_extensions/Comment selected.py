# Comment/Uncomment selected lines

# https://gitlab.com/atronah/pythonista_extensions/tree/master

import editor

text = editor.get_text()
selection = editor.get_line_selection()
selected_text = text[selection[0]:selection[1]]
is_comment = selected_text.strip().startswith('#')
replacement_lines = []
for line in selected_text.splitlines():
    if is_comment: 
        replacement_lines.append(line[1:] if line.strip().startswith('#') 
                                    else line)
    else:
        replacement_lines.append('#' + line)

replacement = '\n'.join(replacement_lines)
editor.replace_text(selection[0], selection[1], replacement)
editor.set_selection(selection[0], selection[0] + len(replacement) - 1)
