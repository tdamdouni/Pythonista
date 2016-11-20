# https://gist.github.com/webvex/0854a663e84863cc5084

# RegExista
# version 1.0
#
# Requires FormElements.py module available at:
#   https://gist.github.com/9e2163e1041a3e17d210
#
# This application uses regular expressions to search
# and replace text. Clipboard text is automatically
# loaded and results are saved back to the clipboard.
# Results can be sent to input for multiple operations.
# Multiline is on and Ignorecase can be toggled.

import clipboard
import cgi
import re
import webbrowser
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from string import Template
from FormElements import *

menu_opt = [['', r''],
            ['Any character', r'.'],
            ['Start of line', r'^'],
            ['End of line', r'$'],
            ['Zero or more of preceding character', r'*'],
            ['One or more of preceding character', r'+'],
            ['Zero or one of preceding character', r'?'],
            ['Number range of preceding character', r'{}'],
            ['Character set', r'[]'],
            ['Group', r'()'],
            ['Alternative (or)', r'|'],
            ['Any decimal digit', r'\d'],
            ['Any non-digit character', r'\D'],
            ['Any whitespace character', r'\s'],
            ['Any non-whitespace character', r'\S'],
            ['Any alphanumeric character', r'\w'],
            ['Any non-alphanumeric character', r'\W'],
            ['Word boundary', r'\b'],
            ['Non-word boundary', r'\B'],
            ['Tab', r'\t'],
            ['Carriage return', r'\r'],
            ['New line', r'\n']]

menu_attrib = ('onchange="getElementById(\'regex\').value += this.value;"' +
              ' onfocus="this.selectedIndex = -1;"')

#form template
HTML = Template('<html><head>' +
  '<style type="text/css">' +
  '  body {margin: 20px 40px; font-family: sans-serif; background: #eee;}' +
  '  input, textarea {font-size: larger;}' +
  '  #source, #regex, #replace_with, #result {font-family: monospace;}' +
  '  #menu {width: 2em;}' +
  '  div {font-variant: small-caps; text-align: right;}' +
  '</style>' +
  '</head><body>' +
  '<form action="/" method="POST" enctype="multipart/form-data">' +
     create_select('menu', menu_opt, menu_attrib) +
     create_textbox('regex', 28) +
  '  &nbsp;&nbsp;' +
     create_checkboxes('case', [['Ignore case', 'on']], '') +
  '  &nbsp;&nbsp;' +
     create_checkboxes('replace', [['Replace with: ', 'on']], '') +
     create_textbox('replace_with', 16) +
  '  &nbsp; &nbsp;' +
  '  <input type="submit" value="Apply" />' +
  '  <br /><br />' +
     create_textarea('source', 88, 12) +
  '  <br /><br />' +
     create_textarea('result', 88, 12) +
  '  <br />' +
     create_checkboxes('swap', [['Send result to input box', 'on']], '') +
  '</form>' +
  '<div> RegExista 1.0 </div>' +
  '</body></html>')

class RequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):  #initial page
		subs = {'regex': '',
		'case_on': '',
		'replace_on': '',
		'replace_with': '',
		'source': clipboard.get(),
		'result': ''}
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		self.wfile.write(HTML.safe_substitute(subs))
		
	def do_POST(self):  #form requests
		#read submitted data
		form = cgi.FieldStorage(fp = self.rfile, headers = self.headers,
		environ = {'REQUEST_METHOD':'POST',
		'CONTENT_TYPE':self.headers['Content-Type']})
		regex = form.getfirst('regex')
		case = str(form.getfirst('case'))
		replace = str(form.getfirst('replace'))
		replace_with = form.getfirst('replace_with')
		source = form.getfirst('source')
		swap = str(form.getfirst('swap'))
		
		#process text
		if case == 'on':  #ignore case
			pattern = re.compile(regex, re.M|re.I)
		else:  #case sensitive
			pattern = re.compile(regex, re.M)
		if replace != 'on':  #search
			result_list = pattern.findall(source)
			result = ''
			for match in result_list:
				result += match + '\n'
		else:  #replace
			result = pattern.sub(replace_with, source)
			
		#prepare response data
		subs = {'regex': regex}
		subs['case_' + case] = 'checked'
		subs['replace_' + replace] = 'checked'
		subs['replace_with'] = replace_with
		if swap != 'on':
			subs['source'] = source
			subs['result'] = result
		else:
			subs['source'] = result
			subs['result'] = ''
		if result != '':
			clipboard.set(result)
			
		#send response
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		self.wfile.write(HTML.safe_substitute(subs))
		
if __name__ == '__main__':
	server = HTTPServer(('', 80), RequestHandler)
	webbrowser.open('http://localhost', stop_when_done = True)
	server.serve_forever()

