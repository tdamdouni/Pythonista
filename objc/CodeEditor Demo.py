# coding: utf-8

# https://gist.github.com/omz/6762c1e55e8c3a596637

'''
NOTE: This requires the latest beta of Pythonista 1.6 (build 160022)

Demo of using Pythonista's own internals to implement an editor view with syntax highlighting (basically the exact same view Pythonista uses itself)

IMPORTANT: This is just for fun -- I was curious if it would work at all, but I don't recommend that you rely on this for anything important. The way Pythonista's internals work can change at any time, and this code is *very* likely to break in the future.
'''

import ui
from objc_util import *

class CodeEditorView (ui.View):
	@on_main_thread
	def __init__(self, mode='python', ext_kb=True, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		valid_modes = {'python': 'OMPythonSyntaxHighlighter', 'html': 'OMHTMLSyntaxHighlighter', 'javascript': 'OMJavaScriptSyntaxHighlighter', 'markdown': 'OMMarkdownSyntaxHighlighter', 'text': 'OMBaseSyntaxHighlighter'}
		if mode not in valid_modes:
			raise ValueError('invalid syntax mode')
		objc_view = ObjCInstance(self._objc_ptr)
		OMTextEditorView = ObjCClass('OMTextEditorView')
		OMSyntaxHighlighterTheme = ObjCClass('OMSyntaxHighlighterTheme')
		SyntaxHighlighter = ObjCClass(valid_modes[mode])
		PA2UITheme = ObjCClass('PA2UITheme')
		theme_dict = PA2UITheme.sharedTheme().themeDict().mutableCopy()
		theme_dict.autorelease()
		theme_dict['font-family'] = 'Menlo-Regular'
		theme_dict['font-size'] = 14
		theme = OMSyntaxHighlighterTheme.alloc().initWithDictionary_(theme_dict)
		theme.autorelease()
		f = CGRect(CGPoint(0, 0), CGSize(self.width, self.height))
		editor_view = OMTextEditorView.alloc().initWithFrame_syntaxHighlighterClass_theme_(f, SyntaxHighlighter, theme)
		editor_view.textView().setAutocapitalizationType_(0)
		editor_view.textView().setAutocorrectionType_(1)
		flex_width, flex_height = (1<<1), (1<<4)
		editor_view.setAutoresizingMask_(flex_width|flex_height)
		margins = UIEdgeInsets(16, 10, 16, 10)
		editor_view.setMarginsForPortrait_landscape_(margins, margins)
		if ext_kb:
			kb_types = {'python': 'KeyboardAccessoryTypePythonCompact', 'markdown': 'KeyboardAccessoryTypeMarkdownWithoutSnippets', 'html': 'KeyboardAccessoryTypeHTML', 'javascript': 'KeyboardAccessoryTypeHTML'}
			kb_type = kb_types.get(mode)
			if kb_type:
				OMKeyboardAccessoryView = ObjCClass('OMKeyboardAccessoryView')
				accessory_view = OMKeyboardAccessoryView.alloc().initWithType_dark_(kb_type, False).autorelease()
				editor_view.setKeyboardAccessoryView_(accessory_view)
		editor_view.autorelease()
		objc_view.addSubview_(editor_view)
		self.editor_view = editor_view
	
	@property
	@on_main_thread
	def text(self):
		text_view = self.editor_view.textView()
		text = text_view.text()
		return unicode(text)
	
	@text.setter
	@on_main_thread
	def text(self, new_text):
		if not isinstance(new_text, basestring):
			raise TypeError('expected string/unicode')
		text_view = self.editor_view.textView()
		text_view.setText_(new_text)
	
	@on_main_thread
	def insert_text(self, text):
		if not isinstance(text, basestring):
			raise TypeError('expected string/unicode')
		text_view = self.editor_view.textView()
		text_view.insertText_(text)
	
	@on_main_thread
	def replace_range(self, range, text):
		text_view = self.editor_view.textView()
		ns_range = NSRange(range[0], range[1]-range[0])
		text_range = ObjCClass('OMTextRange').rangeWithNSRange_(ns_range)
		text_view.replaceRange_withText_(text_range, text)
	
	@property
	@on_main_thread
	def selected_range(self):
		text_view = self.editor_view.textView()
		range = text_view.selectedRange()
		return (range.location, range.location + range.length)
	
	@selected_range.setter
	@on_main_thread
	def selected_range(self, new_value):
		text_view = self.editor_view.textView()
		range = NSRange(new_value[0], new_value[1]-new_value[0])
		text_view.setSelectedRange_(range)
	
	@on_main_thread
	def begin_editing(self):
		text_view = self.editor_view.textView()
		text_view.becomeFirstResponder()
	
	@on_main_thread
	def end_editing(self):
		text_view = self.editor_view.textView()
		text_view.resignFirstResponder()

# --- DEMO

editor_view = None

def copy_action(sender):
	import clipboard
	clipboard.set(editor_view.text)
	import console
	console.hud_alert('Copied')

def main():
	global editor_view
	editor_view = CodeEditorView('python', ext_kb=True, frame=(0, 0, 500, 500))
	editor_view.name = 'Code Editor Demo'
	copy_btn = ui.ButtonItem('Copy', action=copy_action)
	editor_view.right_button_items = [copy_btn]
	editor_view.text = '#coding: utf-8\nprint "Hello World"'
	editor_view.present('sheet')

if __name__ == '__main__':
	main()