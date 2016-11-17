# https://forum.omz-software.com/topic/3201/example-editor-annotate_line-py3-beta

import editor, clipboard, console, io

def get_file_text():
	file_name = editor.get_path()
	with io.open(file_name, encoding = 'utf-8') as file:
		return file.read()
		
def find_lines(text, search_text):
	lst = []
	for ln_no, ln in enumerate(text.splitlines()):
		if search_text in ln:
			lst.append(ln_no + 1)
	return lst
	
def mark_lines(lns, s_text):
	for i, ln in enumerate(lns):
		editor.annotate_line(ln, text = str(i + 1), style = 'success', expanded= False)
		
if __name__ == '__main__':

	s_text = console.input_alert('Enter text to search for')
	if not s_text:
		exit()
		
	file_text = get_file_text()
	
	ln_list = find_lines(file_text, s_text)
	mark_lines(ln_list, s_text)
	
# --------------------

