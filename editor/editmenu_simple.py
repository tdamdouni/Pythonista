# https://gist.github.com/balachandrana/819a324f840dd839b1650aa0bac4402d

import ui
import clipboard, editor

def select_action(self):
	i=editor.get_selection()
	editor.set_selection(i[0],i[1]+1)
	
def copy_action(sender):
	i=editor.get_selection()
	t=editor.get_text()
	clipboard.set(t[i[0]:i[1]])
	
def paste_action(sender):
	i=editor.get_selection()
	t=editor.get_text()
	editor.replace_text(i[0],i[1], clipboard.get())
	editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))
	
def cut_action(sender):
	i=editor.get_selection()
	t=editor.get_text()
	clipboard.set(t[i[0]:i[1]])
	editor.replace_text(i[0],i[1], '')
	editor.set_selection(i[0],i[0])
	
def comment_action(sender):
	"""" comment out selected lines"""
	import re
	COMMENT='#'
	i=editor.get_line_selection()
	t=editor.get_text()
	# replace every occurance of newline with  ewline plus COMMENT, except last newline
	editor.replace_text(i[0],i[1]-1,COMMENT+re.sub(r'\n',r'\n'+COMMENT,t[i[0]:i[1]-1]))
	editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))
	
def uncomment_action(self):
	"""" uncomment selected lines"""
	import re
	COMMENT='#'
	i=editor.get_line_selection()
	t=editor.get_text()
	# replace every occurance of newline # with newline, except last newline
	if all( [x.startswith('#') for x in t[i[0]:i[1]-1].split(r'\n')]):
		editor.replace_text(i[0],i[1]-1,re.sub(r'^'+COMMENT,r'',t[i[0]:i[1]-1],flags=re.MULTILINE))
	editor.set_selection(i[0],i[1]-len(t)+len(editor.get_text()))
	
def execlines_action(self):
	"""execute selected lines in console.   """
	import textwrap
	a=editor.get_text()[editor.get_line_selection()[0]:editor.get_line_selection()[1]]
	exec(textwrap.dedent(a))
	
v = ui.load_view()
v.present('panel')

