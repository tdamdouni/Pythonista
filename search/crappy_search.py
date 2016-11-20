# https://gist.github.com/Phuket2/8223d9f4068d908a097116a0be04c25d

# https://forum.omz-software.com/topic/3252/need-full-text-search-support

'''
        this is crap. i mashed to files together without editing.

        but i could be something. i have just been to lazy to bring it
        together. i use it the wrench menu myself.

        it acually works for meas a quickie when i am looking for a script.
'''

import ui, editor, console, editor
import io, re

# coding: utf-8
import ui, os, scene, io

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_all_styles


# https://gist.github.com/2bbb26b50c980b25bcf4
# last gist update, 00:10 17th Feb, 2016


class CodeDisplay(ui.View):

	def __init__(self, style = 'colorful', use_linenos = True,
	hl_lines = None, *args, **kwargs):
	
		super().__init__(*args, **kwargs)
		
		self.code = ''
		self.code_raw = ''
		self.web_view = None
		self.style = style
		self.use_linenos = use_linenos
		self.hl_lines = hl_lines if hl_lines else list()
		
		self.make_view()
		
	def make_view(self):
		self.web_view = ui.WebView()
		self.web_view.frame = self.bounds
		self.web_view.size_to_fit()
		self.web_view.scales_page_to_fit = True
		self.web_view.flex = 'wh'
		self.add_subview(self.web_view)
		
		
		
	def get_style_names(self):
		return
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
		with io.open(fn, encoding = 'utf-8') as fp:
			code = fp.read()
			
		self.code = code
		self.web_view.load_html(self.get_html(code))
		
	def reload_style(self):
		# stupid hack for now. we rethink this.
		self.load_code_str(self.code)
		#self.update_style_name()
		
	def hilite_lines_with_word(self, word):
		if not word:
			return
		r = []
		w = word.lower()
		for ln, data in enumerate(self.code.splitlines()):
			if w in data.lower():
				r.append(ln + 1)
				
		self.hl_lines = r
		self.reload_style()
		
	def get_html(self, code, use_linenos = None,
	style = None, hl_lines = None):
	
		# returns the html from pygments
		if not use_linenos: use_linenos = self.use_linenos
		if not style: style = self.style
		if not hl_lines : hl_lines = self.hl_lines
		
		lexer = get_lexer_by_name("python", stripall=False)
		formatter = HtmlFormatter(linenos= use_linenos , style = style, hl_lines =hl_lines, full=True)
		return highlight(code, lexer, formatter)
		
		
def preview_Code(fn, word_hilite, *args, **kwargs):
	cd = CodeDisplay(*args, **kwargs)
	cd.load_code_from_file(fn)
	cd.hilite_lines_with_word(word_hilite)
	return cd
	
def called_from_tools_menu():
	'''
	if called from the tools/wrench menu, we just view the current script.
	As i normally use a dark theme, this is ok for me sometimes
	'''
	f = (0,0, 600, 800)
	cd = preview_Code('findfile.py','root', frame = f)
	cd.present('sheet')
	exit()
	
	path = 'v2.py'
	import editor, os
	multipler = .8
	f = (0,0, ui.get_screen_size()[0] * multipler, ui.get_screen_size()[1] * multipler)
	#cd = CodeDisplay(frame = f , hl_lines = range(10, 25))
	cd = CodeDisplay(frame = f )
	cd.load_code_from_file(path)
	#cd.name = fn
	cd.present('sheet')
	cd.hilite_lines_with_word('os.patH')
	
	
	
#from pygments_helper import preview_Code

'''
        Pytonista Forum user @Phuket2
        Python ability - beginner
'''
'''
        /private/var/mobile/Containers/Shared/AppGroup/A83A4237-28DA-41B4-AA91-84BC6770F30C/Pythonista3/Documents/MyProjects/FindTextInSource/show_pyui.py
'''

#_ignore_dirs = ['.Trash', 'Standard Library']
#skip_dirs = '\\.Trash|site-packages|Backup'
skip_dirs = '\\.Trash|Backup'
exts = 'py'
root_dir = os.path.expanduser('~/Documents')


def shorten_path(path, inc_root=False):
	# return minus what we consider the visible root
	if inc_root:
		return path[len(os.path.join(os.path.expanduser('~'), 'Documents')):]
	else:
		return path[len(os.path.expanduser('~')):]
		
		
def allfiles(root_dir, skip_dirs_re=None, file_ext_re=None):
	# from @omz on Pythonista Forums
	for path, subdirs, files in os.walk(root_dir):
		if skip_dirs_re:
			new_subdirs = []
			for subdir in subdirs:
				if not re.match(skip_dirs_re, subdir):
					new_subdirs.append(subdir)
			subdirs[:] = new_subdirs
		for filename in files:
			ext = os.path.splitext(filename)[1][1:]
			if (file_ext_re is None) or (re.match(file_ext_re, ext, re.IGNORECASE)):
				full_path = os.path.join(path, filename)
				yield full_path
				
				
def search_file2(fspec, text):
	with io.open(fspec, 'r', encoding='utf-8') as file:
		if re.search(text, file.read(), re.IGNORECASE):
			return True
		else:
			return False
			
def search_file(fspec, text, ignore_case = True):
	with io.open(fspec, 'r', encoding='utf-8') as file:
		for ln in file.readlines():
			if comp_IGNORECASE(text, ln):
				return True
	return False
	
def comp_IGNORECASE(text, data):
	if text.lower() in data.lower():
		return True
	else:
		return False
		
		
class SearchDisplay(ui.View):
	def __init__(self, file_list, search_term, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.file_list = file_list
		self.search_term = search_term
		self.tv = None
		self.code_preview = None
		self.current_file_name = None
		
		self.make_view()
		
		m_btn = ui.ButtonItem(title='Open In Editor')
		m_btn.action = self.menu_open_in_editor
		self.left_button_items = (m_btn,)
		
		self.right_button_items = ()
		m_btn = ui.ButtonItem(title='Go Back')
		m_btn.action = self.menu_goback
		m_btn.enabled = False
		self.right_button_items = (m_btn,)
		
		self.tv.selected_row = 0
		self.current_file_name = self.file_list[0]
		self.update_title()
		
	def make_view(self):
		tv = ui.TableView(frame=self.bounds)
		tv.flex = 'wh'
		tv.data_source = ui.ListDataSource(self.file_list)
		tv.data_source.tableview_cell_for_row = self.tableview_cell_for_row
		tv.data_source.accessory_action = self.accessory_action
		tv.delegate = tv.data_source
		self.tv = tv
		self.add_subview(tv)
		
	def update_title(self):
		self.name = 'Number of Results = {}'.format(len(self.tv.data_source.items))
		
	def menu_goback(self, sender):
		if self.code_preview:
			self.remove_subview(self.code_preview)
			self.code_preview = None
			self.right_button_items[0].enabled = False
			self.update_title()
			
	def menu_open_in_editor(self, sender):
		if self.current_file_name:
			editor.open_file(self.current_file_name,  True)
			self.close()
			
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell('subtitle')
		item = tableview.data_source.items[row]
		cell.text_label.text = os.path.basename(item)
		cell.detail_text_label.text = shorten_path(item)
		cell.accessory_type = 'detail_button'
		return cell
		
	def accessory_action(self, sender):
		row = sender.tapped_accessory_row
		self.current_file_name = sender.items[row]
		self.tv.selected_row = row
		self.show_preview(sender.items[row])
		
	def show_preview(self, fspec):
		cp = preview_Code(fspec, self.search_term, frame=self.bounds)
		self.name = os.path.basename(fspec)
		self.code_preview = cp
		self.add_subview(cp)
		self.right_button_items[0].enabled = True
		
def find_in_my_source():
	s_txt = console.input_alert('Enter Search String')
	if not s_txt:
		exit()
		
	lst = []
	for fn in allfiles(root_dir=root_dir, skip_dirs_re=skip_dirs,
	file_ext_re=exts ):
		if search_file(fn, s_txt):
			lst.append(fn)
	if not len(lst):
		console.alert('No Natch Found')
		exit()
		
	mc = SearchDisplay(lst, s_txt, frame=f, bg_color='white')
	mc.present(pres, animated=False)
	
if __name__ == '__main__':
	w = 600
	h = 800
	f = (0, 0, w, h)
	pres = 'sheet'
	
	s_txt = console.input_alert('Enter Search String')
	if not s_txt:
		exit()
	lst = []
	for fn in allfiles(root_dir=root_dir, skip_dirs_re=skip_dirs, file_ext_re=exts ):
		if search_file(fn, s_txt):
			lst.append(fn)
	print('Num files found= ', len(lst))
	if not len(lst):
		console.alert('No Natch Found')
		exit()
	#x = MyDataSource(_files)
	#print(dir(x))
	mc = SearchDisplay(lst, s_txt, frame=f, bg_color='white')
	#mc.tv.data_source = x
	#mc.tv.data_source.delegate = x
	mc.present(pres, animated=False)

