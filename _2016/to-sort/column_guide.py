#!python2

# https://gist.github.com/jsbain/278667185d8f23ffd1ed2e48a8d46417

import editor, ui
import _editor_pythonista
from objc_util import *

@on_main_thread
def create_column_guide(num_cols=80):
	''' create vertical line at column index specified.
	TODO:  register for file change notifications, add to all tabs, etc. add ability to remove.
	'''
	ev = _editor_pythonista._get_editor_tab().editorView()
	tv=ev.textView()
	ts=tv.textStorage()
	font=ts.paragraphs()[0].text().fontAttributesInRange_(NSRange(0,0))['NSFont']
	font_char_width=font.advancementForGlyph_(99).width
	# create a 1 pixel "line" view
	v=ui.View(
	frame=(font_char_width*num_cols+tv.gutterWidth(),
	0,1,ev.frame().size.height),
	flex='LH')
	v.border_width=1
	v.alpha=0.1
	ev.addSubview_(ObjCInstance(v))
	return v
	
create_column_guide(80)

