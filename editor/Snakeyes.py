import editor
full_text = editor.get_text()
cursor = editor.get_selection()[1]
while True:
	try:
		if full_text[cursor - 3] + full_text[cursor - 2] + full_text[cursor - 1] == 'def':
			editor.replace_text(cursor, cursor, ' func_name():')
			editor.set_selection(cursor + 1, cursor + 10)
		if full_text[cursor - 3] + full_text[cursor - 2] + full_text[cursor - 1] == 'ifc':
			editor.replace_text(cursor, cursor, ' condition:')
			editor.set_selection(cursor + 1, cursor + 10)
		if full_text[cursor - 3] + full_text[cursor - 2] + full_text[cursor - 1] == 'wlt':
			editor.replace_text(cursor - 2, cursor, 'hile i < num:')
			editor.set_selection(cursor + 7, cursor + 10)
		if full_text[cursor - 3] + full_text[cursor - 2] + full_text[cursor - 1] == 'fea':
			editor.replace_text(cursor - 2, cursor, 'or entry in array:')
			editor.set_selection(cursor + 10, cursor + 15)
		break
	except:
		pass

