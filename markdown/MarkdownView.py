# coding: utf-8

# https://github.com/mikaelho/pythonista-markdownview

from __future__ import print_function
import ui
from markdown2 import markdown
from urllib import quote, unquote
import clipboard
import webbrowser
from string import Template
#from RootView import RootView

class MarkdownView(ui.View):
	
	def __init__(self, frame = None, flex = None, background_color = None, name = None, accessory_keys = True, extras = [], css = None):
		
		if frame: self.frame = frame
		if flex: self.flex = flex
		if background_color: self.background_color = background_color
		if name: self.name = name
		
		self.extras = extras
		self.css = css or self.default_css
		self.proxy_delegate = None
		
		self.enable_links = True
		self.editing = False
		self.margins = (10, 10, 10, 10)
		
		self.link_prefix = 'pythonista-markdownview:relay?content='
		self.debug_prefix = 'pythonista-markdownview:debug?content='
		self.init_postfix = '#pythonista-markdownview-initialize'
		self.in_doc_prefix = ''
		
		self.to_add_to_beginning = ('', -1)
		
		self.backpanel = ui.View()
		self.add_subview(self.backpanel)
		
		# Web fragment is used to find the right scroll position when moving from editing to viewing
		self.web_fragment = ui.WebView()
		self.web_fragment.hidden = True
		self.web_fragment.delegate = MarkdownView.ScrollLoadDelegate()
		self.add_subview(self.web_fragment)

		self.markup = ui.TextView()
		self.add_subview(self.markup)
		self.markup.font = ('<system>', 12)
		
		self.web = ui.WebView()
		self.web.scales_page_to_fit = False 
		self.web.content_mode = ui.CONTENT_TOP_LEFT
		self.add_subview(self.web)
		
		self.web.delegate = self
		self.markup.delegate = self
		
		self.markup.text = ''
		self.update_html()
		self.markup.bounces = False 
		
		# Ghosts are used to determine preferred size
		self.markup_ghost = ui.TextView()
		self.markup_ghost.hidden = True
		#self.add_subview(self.markup_ghost)
		self.web_ghost = ui.WebView()
		self.web_ghost.hidden = True
		#self.add_subview(self.web_ghost)
		
		if accessory_keys:
			self.create_accessory_toolbar()
		
	htmlIntro = Template('''
		<html>
		<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
		<title>Markdown</title>
		<style>
			$css
		</style>
		<script type="text/javascript">
			function debug(msg) {
				var d = document.getElementById("debug");
				d.href="$debug_prefix" + msg;
				d.click();
			}
		
			function activateLinks() {
				content = document.getElementById("content");
				links = content.getElementsByTagName("a");
				for(var i = 0; i < links.length; i++) {
					links[i].addEventListener('click', anchor_click);
				}
			}
			
			function anchor_click() {
				var e = window.event;
				e.stopPropagation();
				return false;
			}
			
			function text_position() {
				var e = window.event;
				var c = document.getElementById("content");
				var r = document.getElementById("relay");
				var range = new Range();
				range.selectNodeContents(c);
				var rangeEnd = document.caretRangeFromPoint(e.clientX, e.clientY);
				range.setEnd(rangeEnd.startContainer, rangeEnd.startOffset);
				r.href="$link_prefix"+encodeURIComponent(range.toString());
				r.click();
			}
			function initialize() {
				//scrollElem = document.getElementById("scroll_here");
				//if (scrollElem) {
					//scrollElem.scrollIntoView();
					//fromTop = scrollElem.getBoundingClientRect().top;
					//window.scrollBy(0, -window.innerHeight/2+fromTop);
				//}
				var scrollPos = $scroll_pos;
				if (scrollPos > -1) {
					var totalHeight = document.getElementById("content").clientHeight;		
					var halfScreen = window.innerHeight/2;
					if ((totalHeight - scrollPos) > halfScreen) {
						scrollPos -= halfScreen;
					}
					window.scrollBy(0, scrollPos);
					activateLinks();
					var r = document.getElementById("relay");
					r.href = "$init_postfix"
					r.click()
				}
			}
		</script>
		</head>
		<body onload="initialize()">
			<a id="relay" style="display:none"></a>
			<a id="debug" style="display:none"></a>
			<div id="content" onclick="text_position()">
	''')
	htmlOutro = '''
			</div>
		</body>
		</html>
	'''
	default_css = '''
		* {
			font-size: $font_size;
			font-family: $font_family;
			color: $text_color;
			text-align: $text_align;
			-webkit-text-size-adjust: none;
			-webkit-tap-highlight-color: transparent;
		}
		h1 {
			font-size: larger;
		}
		h3 {
			font-style: italic;
		}
		h4 {
			font-weight: normal;
			font-style: italic;
		}
		code {
			font-family: monospace;
		}
		li {
			margin: .4em 0;
		}
		body {
			#line-height: 1;
			background: $background_color;
		}
	'''
		
	def to_html(self, md = None, scroll_pos = -1, content_only = False):
		md = md or self.markup.text
		result = markdown(md, extras=self.extras)
		if not content_only:
			intro = Template(self.htmlIntro.safe_substitute(css = self.css))
			(font_name, font_size) = self.font
			result = intro.safe_substitute(
				background_color = self.to_css_rgba(self.markup.background_color), 
				text_color = self.to_css_rgba(self.markup.text_color),
				font_family = font_name,
				text_align = self.to_css_alignment(),
				font_size = str(font_size)+'px',
				init_postfix = self.init_postfix,
				link_prefix = self.link_prefix,
				debug_prefix = self.debug_prefix,
				scroll_pos = scroll_pos
			) + result + self.htmlOutro
		return result
		
	def to_css_rgba(self, color):
		return 'rgba({:.0f},{:.0f},{:.0f},{})'.format(color[0]*255, color[1]*255, color[2]*255, color[3])

	def to_css_alignment(self):
		mapping = { ui.ALIGN_LEFT: 'left', ui.ALIGN_CENTER: 'center', ui.ALIGN_RIGHT: 'right', ui.ALIGN_JUSTIFIED: 'justify', ui.ALIGN_NATURAL: 'start' }
		return mapping[self.markup.alignment]
		
	def update_html(self):
		html = self.to_html(self.markup.text, 0)
		self.web.load_html(html)
		html_ghost = self.to_html(self.markup.text)
		self.web_fragment.load_html(html_ghost)
		
		'''ACCESSORY TOOLBAR'''
	
	def create_accessory_toolbar(self):
		from objc_util import ObjCClass, ObjCInstance, sel
		
		def create_button(label, func):
			button_width = 25
			black = ObjCClass('UIColor').alloc().initWithWhite_alpha_(0.0, 1.0)
			action_button = ui.Button()
			action_button.action = func
			accessory_button = ObjCClass('UIBarButtonItem').alloc().initWithTitle_style_target_action_(label, 0, action_button, sel('invokeAction:'))
			accessory_button.width = button_width
			accessory_button.tintColor = black
			return (action_button, accessory_button)
		
		vobj = ObjCInstance(self.markup)

		keyboardToolbar = ObjCClass('UIToolbar').alloc().init()
		
		keyboardToolbar.sizeToFit()
		
		button_width = 25
		black = ObjCClass('UIColor').alloc().initWithWhite_alpha_(0.0, 1.0)
		
		# Create the buttons
		# Need to retain references to the buttons used
		# to handle clicks
		(self.indentButton, indentBarButton) = create_button(u'\u21E5', self.indent)
		
		(self.outdentButton, outdentBarButton) = create_button(u'\u21E4', self.outdent)
		
		(self.quoteButton, quoteBarButton) = create_button('>', self.block_quote)
		
		(self.linkButton, linkBarButton) = create_button('[]', self.link)
		
		#(self.anchorButton, anchorBarButton) = create_button('<>', self.anchor)
		
		(self.hashButton, hashBarButton) = create_button('#', self.heading)
		
		(self.numberedButton, numberedBarButton) = create_button('1.', self.numbered_list)
		
		(self.listButton, listBarButton) = create_button('•', self.unordered_list)
		
		(self.underscoreButton, underscoreBarButton) = create_button('_', self.insert_underscore)
		
		(self.backtickButton, backtickBarButton) = create_button('`', self.insert_backtick)
		
		# Flex between buttons
		f = ObjCClass('UIBarButtonItem').alloc().initWithBarButtonSystemItem_target_action_(5, None, None)
		
		doneBarButton = ObjCClass('UIBarButtonItem').alloc().initWithBarButtonSystemItem_target_action_(0, vobj, sel('endEditing:')) 
		
		keyboardToolbar.items = [indentBarButton, f, outdentBarButton, f, quoteBarButton, f, linkBarButton, f, hashBarButton, f, numberedBarButton, f, listBarButton, f, underscoreBarButton, f, backtickBarButton, f, doneBarButton]
		vobj.inputAccessoryView = keyboardToolbar
	
	def indent(self, sender):
		def func(line):
			return '  ' + line
		self.transform_lines(func)
		
	def outdent(self, sender):
		def func(line):
			if str(line).startswith('  '):
				return line[2:]
		self.transform_lines(func, ignore_spaces = False)
	
	def insert_underscore(self, sender):
		self.insert_character('_', '___')
		
	def insert_backtick(self, sender):
		self.insert_character('`', '`')
		
	def insert_character(self, to_insert, to_remove):
		tv = self.markup
		(start, end) = tv.selected_range
		(r_start, r_end) = (start, end)
		r_len = len(to_remove)
		if start <> end:
			if tv.text[start:end].startswith(to_remove):
				if end - start > 2*r_len + 1 and tv.text[start:end].endswith(to_remove):
					to_insert = tv.text[start+r_len:end-r_len]
					r_end = end-2*r_len
			elif start-r_len > 0 and tv.text[start-r_len:end].startswith(to_remove):
				if end+r_len <= len(tv.text) and tv.text[start:end+r_len].endswith(to_remove):
					to_insert = tv.text[start:end]
					start -= r_len
					end += r_len
					r_start = start
					r_end = end-2*r_len
			else:
				r_end = end + 2*len(to_insert)
				to_insert = to_insert + tv.text[start:end] + to_insert
		tv.replace_range((start, end), to_insert)
		if start <> end:
			tv.selected_range = (r_start, r_end)
		
	def heading(self, sender):
		def func(line):
			return line[3:] if str(line).startswith('###') else '#' + line
		self.transform_lines(func, ignore_spaces = False)
		
	def numbered_list(self, data):
		def func(line):
			if line.startswith('1. '):
				return line[3:]
			else:
				return '1. ' + (line[2:] if line.startswith('* ') else line)
		self.transform_lines(func)
		
	def unordered_list(self, sender):
		def func(line):
			if str(line).startswith('* '):
				return line[2:]
			else:
				return '* ' + (line[3:] if line.startswith('1. ') else line)
		self.transform_lines(func)
		
	def block_quote(self, sender):
		def func(line):
			return '> ' + line
		self.transform_lines(func, ignore_spaces = False)
		
	def link(self, sender):
		templ = "[#]($)"
		(start, end) = self.markup.selected_range
		templ = templ.replace('$', self.markup.text[start:end])
		new_start = start + templ.find('#')
		new_end = new_start + (end - start)
		templ = templ.replace('#', self.markup.text[start:end])
		self.markup.replace_range((start, end), templ)
		self.markup.selected_range = (new_start, new_end)
		
	'''
	OBSOLETE: Use heading-ids or toc markdown extra instead
	
	* __<>__ - In-document links - Creates an anchor (`<a>` tag) after the selection, assumed to be some heading text. At the same time, places a link to the anchor on the clipboard, typically to be pasted in a table of contents.
	'''
	def anchor(self, sender):
		templ = " <a name='#'></a>"
		(start, end) = self.markup.selected_range
		link_label = self.markup.text[start:end]
		link_name = quote(self.markup.text[start:end])
		templ = templ.replace('#', link_name)
		self.markup.replace_range((end, end), templ)
		link = "[" + link_label + "](#" + link_name + ")"
		clipboard.set(link)
		
	def make_list(self, list_marker):
		self.get_lines()
		
	def transform_lines(self, func, ignore_spaces = True):
		(orig_start, orig_end) = self.markup.selected_range
		(lines, start, end) = self.get_lines()
		replacement = []
		for line in lines:
			spaces = ''
			if ignore_spaces:
				space_count = len(line) - len(line.lstrip(' '))
				if space_count > 0:
					spaces = line[:space_count]
					line = line[space_count:]
			replacement.append(spaces + func(line))
		self.markup.replace_range((start, end), '\n'.join(replacement))
		new_start = orig_start + len(replacement[0]) - len(lines[0])
		if new_start < start:
			new_start = start
		end_displacement = 0
		for index, line in enumerate(lines):
			end_displacement += len(replacement[index]) - len(line)
		new_end = orig_end + end_displacement
		if new_end < new_start:
			new_end = new_start
		self.markup.selected_range = (new_start, new_end)
		
	def get_lines(self):
		(start, end) = self.markup.selected_range
		text = self.markup.text
		new_start = text.rfind('\n', 0, start)
		new_start = 0 if new_start == -1 else new_start + 1
		new_end = text.find('\n', end)
		if new_end == -1: new_end = len(text)
		#else: new_end -= 1
		if new_end < new_start: new_end = new_start
		return (text[new_start:new_end].split('\n'), new_start, new_end)
	
	def layout(self):
		(top, left, bottom, right) = self.margins
		self.backpanel.frame = (0, 0, self.width, self.height)
		self.markup.frame = (left, top, self.width - left - right, self.height - top - bottom)
		self.web.frame = self.markup.frame
		
	def start_editing(self, words):
		if not self.markup.editable:
			return 
		self.web.hidden = True
		self.editing = True
		caret_pos = 0
		marked = self.markup.text
		for word in words:
			caret_pos = marked.find(word, caret_pos) + len(word)
		self.markup.begin_editing()
		self.markup.selected_range = (caret_pos, caret_pos)
		
	'''VIEW PROXY PROPERTIES'''
	
	@property
	def background_color(self):
		return self.markup.background_color
	@background_color.setter
	def background_color(self, value):
		self.markup.background_color = value
		self.backpanel.background_color = value
		#self.background_color = value
		self.update_html()	
		
	'''SIZING METHODS'''
	
	
	def size_to_fit(self, using='current', min_width=None, max_width=None, min_height=None, max_height=None):
		(self.width, self.height) = self.preferred_size(using)
			
	def preferred_size(self, using='current', min_width=None, max_width=None, min_height=None, max_height=None):
		
		if using=='current':
			using = 'markdown' if self.editing else 'html'
				
		if using=='markdown':
			self.markup_ghost.text = self.markup.text
			view = self.markup_ghost
		else:
			view = self.web_ghost
		
		view.size_to_fit()
		if max_width and view.width > max_width:
			view.width = max_width
			view.size_to_fit()
		if max_width and view.width > max_width:
			view.width = max_width
		if min_width and view.width < min_width:
			view.width = min_width
		if max_height and view.height > max_height:
			view.height = max_height
		if min_height and view.height < min_height:
			view.height = min_height

		return (view.width, view.height)
		
		
	'''TEXTVIEW PROXY PROPERTIES'''
		
	@property
	def alignment(self):
		return self.markup.alignment
	@alignment.setter
	def alignment(self, value):
		self.markup.alignment = value
		self.update_html()
		
	@property
	def autocapitalization_type(self):
		return self.markup.autocapitalization_type
	@autocapitalization_type.setter
	def autocapitalization_type(self, value):
		self.markup.autocapitalization_type = value
		
	@property
	def autocorrection_type(self):
		return self.markup.autocorrection_type
	@autocorrection_type.setter
	def autocorrection_type(self, value):
		self.markup.autocorrection_type = value
		
	@property
	def auto_content_inset(self):
		return self.markup.auto_content_inset
	@auto_content_inset.setter
	def auto_content_inset(self, value):
		self.markup.auto_content_inset = value
		
	@property
	def delegate(self):
		return self.proxy_delegate
	@delegate.setter
	def delegate(self, value):
		self.proxy_delegate = value
		
	@property
	def editable(self):
		return self.markup.editable
	@editable.setter
	def editable(self, value):
		self.markup.editable = value
		
	@property
	def font(self):
		return self.markup.font
	@font.setter
	def font(self, value):
		self.markup.font = value
		self.update_html()
		
	@property
	def keyboard_type(self):
		return self.markup.keyboard_type
	@keyboard_type.setter
	def keyboard_type(self, value):
		self.markup.keyboard_type = value
		
	@property
	def selectable(self):
		return self.markup.selectable
	@selectable.setter
	def selectable(self, value):
		self.markup.selectable = value
		
	@property
	def selected_range(self):
		return self.markup.selected_range
	@selected_range.setter
	def selected_range(self, value):
		self.markup.selected_range = value
		
	@property
	def spellchecking_type(self):
		return self.markup.spellchecking_type
	@spellchecking_type.setter
	def spellchecking_type(self, value):
		self.markup.spellchecking_type = value
		
	@property
	def text(self):
		return self.markup.text
	@text.setter
	def text(self, value):
		self.markup.text = value
		self.update_html()
		
	@property
	def text_color(self):
		return self.markup.text_color
	@text_color.setter
	def text_color(self, value):
		self.markup.text_color = value
		self.update_html()
		
	'''TEXTVIEW PROXY METHODS'''
		
	def replace_range(self, range, text):
		self.markup.replace_range(range, text)
		self.update_html()
		
	'''WEBVIEW PROXY PROPERTIES'''
	
	@property
	def scales_page_to_fit(self):
		return self.web.scales_page_to_fit
	@scales_page_to_fit.setter
	def scales_page_to_fit(self, value):
		self.web.scales_page_to_fit = value
		
	#def keyboard_frame_did_change(self, frame):
		#if self.custom_keys:
			#self.custom_keys.change(frame, self.markup)
	
	def can_call(self, func_name):
		if not self.proxy_delegate:
			return False
		return callable(getattr(self.proxy_delegate, func_name, None))
	
	'''TEXTVIEW DELEGATES'''
	def textview_did_end_editing(self, textview):
		(start, end) = self.markup.selected_range
		html_fragment = self.to_html(self.markup.text[0:start])
		self.web_fragment.frame = self.web.frame
		self.web_fragment.delegate.end_edit = True
		self.web_fragment.load_html(html_fragment)

	class ScrollLoadDelegate():
		def __init__(self):
			self.end_edit = False
		def webview_did_finish_load(self, webview):
			if not self.end_edit: return
			self.end_edit = False
			
			m = webview.superview
			scroll_pos = int(webview.eval_js('document.getElementById("content").clientHeight'))
			html = m.to_html(m.markup.text, scroll_pos)
			m.web.load_html(html)
			html_ghost = m.to_html(m.markup.text)
			m.web_ghost.load_html(html_ghost)
			#m.web.hidden = False
			m.editing = False
			if m.can_call('textview_did_end_editing'):
				m.proxy_delegate.textview_did_end_editing(textview)
			
	def textview_should_change(self, textview, range, replacement):
		should_change = True
		self.to_add_to_beginning = ('', -1)
		if self.can_call('textview_should_change'):
			should_change =  self.proxy_delegate.textview_should_change(textview, range, replacement)
		if should_change == True and replacement == '\n': #and range[0] == range[1] 
			pos = range[0]
			next_line_prefix = ''
			# Get to next line
			pos = self.markup.text.rfind('\n', 0, pos)
			if not pos == -1:
				pos = pos + 1
				rest = self.markup.text[pos:]
				# Copy leading spaces
				space_count = len(rest) - len(rest.lstrip(' '))
				if space_count > 0:
					next_line_prefix += rest[:space_count]
					rest = rest[space_count:]
				# Check for prefixes
				prefixes = [ '1. ', '+ ', '- ', '* ']
				for prefix in prefixes:
					if rest.startswith(prefix):
						next_line_prefix += prefix
						break
				if len(next_line_prefix) > 0:
					diff = range[0] - pos
					if diff < len(next_line_prefix):
						next_line_prefix = next_line_prefix[:diff]
					self.to_add_to_beginning = (next_line_prefix, range[0]+1)		
		return should_change
			
	def textview_did_change(self, textview):
		add = self.to_add_to_beginning
		if add[1] > -1:
			self.to_add_to_beginning = ('', -1)
			self.markup.replace_range((add[1], add[1]), add[0])
		if self.can_call('textview_did_change'):
			self.proxy_delegate.textview_did_change(textview)
			
	def textview_should_begin_editing(self, textview):
		if self.can_call('textview_should_begin_editing'):
			return self.proxy_delegate.textview_should_begin_editing(textview)
		else:
			return True
	def textview_did_begin_editing(self, textview):
		if self.can_call('textview_did_begin_editing'):
			self.proxy_delegate.textview_did_begin_editing(textview)
	
	def textview_did_change_selection(self, textview):
		if self.can_call('textview_did_change_selection'):
			self.proxy_delegate.textview_did_change_selection(textview)
			
	'''WEBVIEW DELEGATES'''
	
	def webview_should_start_load(self, webview, url, nav_type):
		# Click, should start edit in markdown
		if url.startswith(self.link_prefix):
			left_side = unquote(url.replace(self.link_prefix, ''))
			self.start_editing(left_side.split())
			#webview.stop()
			return False
		# Debug message from web page, print to console
		elif url.startswith(self.debug_prefix):
			debug_text = unquote(url.replace(self.debug_prefix, ''))
			print(debug_text)
			return False
		# Loaded by the web view at start, allow
		elif url.startswith('about:blank'):
			return True
		# Custom WebView initialization message
		# Used to check if in-doc links starting with '#'
		# have extra stuff in front
		elif url.endswith(self.init_postfix):
			self.in_doc_prefix = url[:len(url)-len(self.init_postfix)]
			self.web.hidden = False
			return False
			
		# If link starts with the extra stuff detected
		# at initialization, remove the extra
		if url.startswith(self.in_doc_prefix):
			url = url[len(self.in_doc_prefix):]
		
		# Check for custom link handling
		if self.can_call('webview_should_start_load'):
			return self.proxy_delegate.webview_should_start_load(webview, url, nav_type)
		# Handle in-doc links within the page
		elif url.startswith('#'):
			if self.can_call('webview_should_load_internal_link'):
				return self.proxy_delegate.webview_should_load_internal_link(webview, url)
			return True
		# Open 'http(s)' links in Safari
		# 'file' in built-in browser
		# Others like 'twitter' as OS decides
		else:
			if self.can_call('webview_should_load_external_link'):
				return self.proxy_delegate.webview_should_load_external_link(webview, url)
			if url.startswith('http:') or url.startswith('https:'):
				url = 'safari-' + url
			webbrowser.open(url)
			return False
		
	def webview_did_start_load(self, webview):
		if self.can_call('webview_did_start_load'):
			self.proxy_delegate.webview_did_start_load(webview)
	def webview_did_finish_load(self, webview):
		#if not self.editing:
			#self.web.hidden = False
		if self.can_call('webview_did_finish_load'):
			self.proxy_delegate.webview_did_finish_load(webview)
	def webview_did_fail_load(self, webview, error_code, error_msg):
		if self.can_call('webview_did_fail_load'):
			self.proxy_delegate.webview_did_fail_load(webview, error_code, error_msg)
				
### CUT HERE - everything below this line is for demonstration only and can be removed for production

if __name__ == "__main__":
	import os
	readme_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'readme.md')
	class SaveDelegate (object):
		def textview_did_change(self, textview):
			with open(readme_filename, "w") as file_out:
				file_out.write(textview.text)
	init_string = ''
	
	markdown_edit = MarkdownView(extras = ["header-ids"])
	# Use this if you do not want accessory keys:
	#markdown_edit = MarkdownView(accessory_keys = False)
	markdown_edit.name = 'MarkdownView Documentation'
	
	if os.path.exists(readme_filename):
		with open(readme_filename) as file_in:
			init_string = file_in.read()
	markdown_edit.text = init_string
	markdown_edit.delegate = SaveDelegate()
	
	markdown_edit.font = ('Apple SD Gothic Neo', 16)
	markdown_edit.background_color = '#f7f9ff'
	markdown_edit.text_color = '#030b60'
	markdown_edit.margins = (10, 10, 10, 10)
	
	# Examples of other attributes to set:
	#markdown_edit.alignment = ui.ALIGN_JUSTIFIED
	#markdown_edit.editable = False
	
	markdown_edit.present(style='fullscreen', hide_title_bar=False) 
