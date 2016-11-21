# coding: utf-8

# https://gist.github.com/Phuket2/2bbb26b50c980b25bcf4

import ui
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_all_styles


"""
	a pygments helper, wrapper or whatever you want it call it. 
	
	should be both a helper class as well as a code previewer
	
	idea 1: (code preview)
		add to your tools menu. if called from the tools menu, the current
		script is displayed fullscreen. why? i use a dark theme, which is 
		really good for writing in, but not as great for reviewing code.
		its just nice to see it in a lighter theme sometimes for a quick
		review. maybe, thats just me. but i like it.
		
		
	idea 2 (searching for phrases in .py files)
		i am writing a filehelper. it includes a search function for
		text/phrases specifically in .py files. but not limited to. So when
		finished this class will display a given selected file from a
		ui.table. The lines where the phrase appears will be hilited.  
		i am sure can get to the word/phrase level also...but later

	idea 3 (is for anyone to use, or at least get started with pygments)
		just sometimes if something is presented to you, even it 
		doesnt work that well, it can still spark ideas. 
	
"""


class pop_up_menu(ui.View):
	# displays a popup menu, with a ui.Table
	# hope to make it generic later
	# not trying to position the popup yet
	def __init__(self, parent, items, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
		self.tb = None
		self.items = items
		self.parent = parent
		
		self._create_view()
		
	def _create_view(self):
		tb = ui.TableView(name = 'style_table')
		ls = ui.ListDataSource(items = self.items)
		tb.data_source = ls
		tb.delegate = tb.data_source
		ls.action = self.row_selected
		self.tb = tb
		self.add_subview(tb)
	
	def layout(self):
		self.tb.frame = self.bounds
		
	def display(self):
		self.present('popover')
	
	def row_selected(self, sender):
		item = sender.items[sender.selected_row]
		self.parent._callback_popup_menu_selection(item)
		self.close()
	
	
		
	
class CodeDisplay(ui.View):
	def __init__(self, style = 'colorful', use_linenos = True,
	*args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
		self.code = None
		self.web_view = None
		self.style = style
		self.use_linenos = use_linenos
		
		self.tool_menu = None
		self.tool_btn_h = 36
		
		self._create_view_items()
		self.update_style_name()
		
	def _create_view_items(self):
		self.web_view = ui.WebView()
		self.web_view.size_to_fit()
		self.web_view.scales_page_to_fit = True
		self.add_subview(self.web_view)
		self.tool_menu = self.create_tool_bar()
		self.add_subview(self.tool_menu)
		
	def create_tool_bar(self):
		v = ui.View(name = 'tool_bar')
		v.bg_color = 'pink'
		btn = ui.Button(name = 'style', title = 'Styles')
		btn.frame = (0,0,90, 32)
		btn.image = ui.Image.named('iob:arrow_down_b_32')
		btn.action = self._show_style_menu
		v.add_subview(btn)
		
		lb = ui.Label(name = 'style_label')
		lb.frame = (10, 2, 200, 32)
		lb.text_color = btn.tint_color
		v.add_subview(lb)
		
		return v
		
		
	def update_style_name(self):
		self.tool_menu['style_label'].text = 'Style: ' + self.style
		
		
	def _show_style_menu(self, sender):
		#print sender.name
		#show_style_menu(self.get_style_names())
		f = (0,0, 350, 600)
		pop_up_menu(self, self.get_style_names(), name = 'Styles', frame = f).display()
		
	def layout(self):
		if self.superview:
			self.frame = superview.bounds
		
		# postion/size the tool_bar
		f = (0,0, self.width, self.tool_btn_h)
		self.tool_menu.frame = f
		btn = self.tool_menu['style']
		btn.x = self.tool_menu.width -(btn.width + 10)
		
		# postion/size the WebView
		f = (0,self.tool_btn_h, self.width, self.height - self.tool_btn_h)
		self.web_view.frame = f

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
		
	def load_code_str(self, code):
		# load python code as a string into the webview
		self.code = code
		self.web_view.load_html(self.get_html(code))

	def load_code_from_file(self, fn):
		# load a file into the webview
		code = ''
		with open(fn) as fp:
			code = fp.read()
		
		self.code = code
		self.web_view.load_html(self.get_html(code))
		
	def reload_style(self):
		# stupid hack for now. we rethink this. 
		self.load_code_str(self.code)
		self.update_style_name()
		
	def get_html(self, code, use_linenos = None,
					style = None, hl_lines = None):

		if not use_linenos: use_linenos = self.use_linenos
		if not style: style = self.style
		if not hl_lines : hl_lines = list()

		lexer = get_lexer_by_name("python", stripall=False)
		formatter = HtmlFormatter(linenos= use_linenos , style = style, hl_lines =hl_lines, full=True)
		return highlight(code, lexer, formatter)
	
	def _callback_popup_menu_selection(self, item):
		# call back from the pop_up_menu
		# many ideas how to implement this, thinking on it...
		# a delegate style would probably the smartest, i guess
		self.style = item
		self.reload_style()
	

def called_from_tools_menu():
	'''
	if called from the tools/wrench menu, we just view the current script.
	As i normally use a dark theme, this is ok for me sometimes
	'''
	import editor, os
	cd = CodeDisplay()
	path = editor.get_path()
	dir, fn = os.path.split(path)
	cd.load_code_from_file(path)
	cd.name = fn
	cd.present('')
	
	
if __name__ == '__main__':
	
	called_from_tools_menu()
	