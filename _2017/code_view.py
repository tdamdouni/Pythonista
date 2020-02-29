# coding: utf-8

# https://gist.github.com/Phuket2/4ca94bb3d76e80cee6a3

from __future__ import print_function
import ui

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_all_styles

class CodeDisplay(ui.View):
	def __init__(self, style = 'colorful', use_linenos = True,
							code = '', *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
		self.code = code
		self.web_view = None
		self.style = style
		self.use_linenos = use_linenos
		
		self._create_view_items()
		self.load_code_str()
		
	def _create_view_items(self):
		self.web_view = ui.WebView()
		self.web_view.size_to_fit()
		self.web_view.scales_page_to_fit = True
		self.add_subview(self.web_view)
	
	def layout(self):
		self.web_view.frame = self.bounds
	
	def get_style_names(self):
		#return [s for s in get_all_styles()]

		# i stopped with list comp. i think get_all_styles(), was causing 
		# Pythonista to crash. tried many times. its was during editing, so
		# i think some code executing on the import. creating the problem.
		# but just guessing
		lst = []
		for style in get_all_styles():
			lst.append(style)
		
		return sorted(lst)
		
	def load_code_str(self):
		# load python code as a string into the webview
		self.web_view.load_html(self.get_html(self.code))
		
	def get_html(self, code, use_linenos = None,
					style = None, hl_lines = None):
						
		# returns the html from pygments
		if not use_linenos: use_linenos = self.use_linenos
		if not style: style = self.style
		
		lexer = get_lexer_by_name("python", stripall=False)
		formatter = HtmlFormatter(linenos=use_linenos , style=style,  full=True)
		return highlight(code, lexer, formatter)
	
		
	
if __name__ == '__main__':
	# example usage
	import editor
	f = (0,0, ui.get_screen_size()[0] * .8, ui.get_screen_size()[1] * .8)
	path = editor.get_path()
	with open(path) as file:
		code = file.read()
		
	cd = CodeDisplay(frame = f, name = 'Snippet x', code = code)
	
	cd.present('sheet', animated = False)
	
	# left this in just so easy to see the different style names
	print(cd.get_style_names())
	
	
