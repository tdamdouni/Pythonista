# https://gist.github.com/danrcook/7b7076fc419a53832b67321e5ba075f4

import re
import difflib
import cgi

class HtmlDiff(object):
	'''Will take two version of text and present a git style diff in html format (useful to present in a ui.webview)'''
	def __init__(self, a, b):
		self.diff = [line for line in difflib.ndiff(cgi.escape(a).splitlines(), cgi.escape(b).splitlines())]
		self.html = self.diff_to_html(self.diff)
		self.css = '''<style>body {margin:0 0} .t {display:table; width:100%; padding:0} .tr {display:table-row;} pre {font:12px Consolas, "Liberation Mono", Menlo, Courier, monospace; color: #666666; white-space:pre-wrap; tab-size:4}      .plus {background-color:#a6f3a6; border-radius:1px; border-bottom:2px solid #5aee5a; } .minus {background-color:#f8cbcb; border-radius:1px; border-bottom:2px solid #ee5a5a;} .normal, .red, .green{display:table-cell; width:5%; color:grey; font-family: courier; font-size:10pt; margin:0 5px; text-align:right;} .normal {background-color: #fdfdfd; border-right: 1px solid #eee} .red {background-color: #ffdddd; border-right: 1px solid #f1c0c0} .green {background-color: #dbffdb; border-right:1px solid #c1e9c1} .redmain {display:table-cell; background-color: #ffecec;} .greenmain {display:table-cell; background-color: #eaffea;} .normalmain {display:table-cell; background-color: #fdfdfd;} div {padding:4px 4px}</style>'''
		
	def span_insert(self, line, indicator, hl_type, ll=0):
		text = re.compile('\^+|\++|\-+')
		for m in text.finditer(indicator):
			line = line[:m.start()+ll] + '<span class="{}">'.format(hl_type) + line[m.start()+ll:m.end()+ll] + '</span>' + line[m.end()+ll:]
			ll += len('<span class="{}"'.format(hl_type)) + len('</span>')
		return line
		
	def return_div(self, num1='&nbsp;', num2='&nbsp;', color='', text=''):
		div_line = '<div class="{nc}">{n1}</div><div class="{nc}">{n2}</div><div class="{mc}"><pre>{t}</pre></div>'.format(nc=color, n1=str(num1), n2=str(num2), mc=color+'main', t=text)
		return div_line
		
	def diff_to_html(self, diff, a_line=1, b_line=1, text=''):
		for n, line in enumerate(diff):
			text += '<div class="tr">'
			plus_line, minus_line, question_line = line.startswith('+'), line.startswith('-'), line.startswith('?')
			next_line_question = diff[n+1].startswith('?') if n+1<len(diff) else False
			text += self.return_div(color='red', num1=a_line, text=self.span_insert(line, diff[n+1], hl_type="minus")) if all([minus_line, next_line_question]) else ''
			text += self.return_div(color='green', num2=b_line, text=self.span_insert(line, diff[n+1], hl_type="plus")) if all([plus_line, next_line_question]) else ''
			text += self.return_div(color='red', num1=a_line, text=line) if minus_line and not next_line_question else ''
			text += self.return_div(color='green', num2=b_line, text=line) if plus_line and not next_line_question else ''
			text += self.return_div(color='normal', num1=a_line, num2=b_line, text=line) if all([not next_line_question, not plus_line, not minus_line, not question_line]) else ''
			a_line += 1 if minus_line or all([not next_line_question, not plus_line, not minus_line, not question_line]) else 0
			b_line += 1 if plus_line or all([not next_line_question, not plus_line, not minus_line, not question_line]) else 0
			text += '</div>'
		return '<div class="t">{}</div>'.format(text)
		
	def output(self):
		return self.css + self.html if self.html else ''
		
		
if __name__ == '__main__':
	'''simple interface to select two files from the current directory and displaying their diff'''
	import dialogs
	import os
	import ui
	
	file_list = os.listdir(os.getcwd())
	file_a = dialogs.list_dialog('Pick File A (old version)', file_list)
	file_list.remove(file_a)
	file_b = dialogs.list_dialog('Pick File B (new version)', file_list)
	with open(file_a, 'r') as file:
		file_a_text = file.read()
	with open(file_b, 'r') as file:
		file_b_text = file.read()
		
	html = HtmlDiff(file_a_text, file_b_text).output()
	
	w = ui.WebView()
	w.load_html(html)
	w.scales_page_to_fit = False
	w.present()

