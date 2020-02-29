from __future__ import print_function
# https://gist.github.com/mcsquaredjr/4450031

# Interactive multimarkdown table generator. 

# 1/3/13 created
# Copyright (c) by McSquaredJr.
# Normalization code is by Dr. Drang http://goo.gl/DTphm

import cgi
import zlib
import webbrowser
import clipboard
from bs4 import BeautifulSoup, Tag
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

"""Interactive multimarkdown table generator. Please note that 
multi-column spanning is not supported in this version. I need
some time to think how to implement it in a sensible way.

To change text alignment press on the alignment button. Generated
code will be placed in the clipboard.

Dr. Drang's code is used for table 'normalization', see
http://goo.gl/DTphm for details.
"""

# Max table dimensions
MAX_DIM = 30

style_str_zip = """\
x\x9c\xc5\x96Ko\xdb8\x10\xc7\xcf\xfe\x16\x83\x18A\x1a\xc0\x12$;^\'2\xf6Pt\x0f[\xa0\r\n\xec\x1e\xf6J\x89#\x9b\x08E\n$\xfdj\xd1\xef^\xbe"\xcb\x8f\xec6Y/V\x82ek\x86\x9c\x19\r\x7f\xfc[\x00\xcb1|\x83A-\x85Ij\xd20\xbe+\xae>\xef\x14#\x14\xbe(y5\x82p3\x82\xabO\xacDE\x0c\x93\x02\xfe B[\xd7\xd5#k\xca\x95\xf6\xb7\xf0\xc9\x19~G\xbeF\xc3*\x02\x8f\xb8Bk\xe9\x0c#xo\xe3\xf0\x11h;8\xd1\xa8X=\x8fi5\xfb\x8a\xc5$k\xb7s\x80\x81\xc1\xadI\x08g\x0bQT(\x0c\xaa9|\x07XqW$g\xda\x8e6;\x8e\x89\xd9\xb5X\x80\x90\x02\xbd\xbfU\xe8\x06l\x96\xcc`\xa2[RY\xa7\xb5%\x1bE\xda\xf9\x91=\x91I\xcf\xb5\xaf \x9f\xba\n\x06\rQ\x0b&\x12\x8e\xb5)rl\xac\xa5\x94\x8a\xa2*\xb4\xe4\x8cB\xdenaHHU\xe3\x9ds\x91\xeai\xa1\xe4J\xd0\x02\x86\xf5\xcc\x9d\xee!ZB)\x13\x8b\x02\xb2\xd4\x86\xb0\xd7\xa9\xbfN\xfcu\xd6\x0b\x1a\xd2@\xee\xa2\x86\xf8\xfb\xd8\xa1\x10\xebt3 {\xfevQ\xacW\xaeQ\xd5\\n\n +#\xdd32j\x96\x05<L\xae}G([\xbb\x8e\xf4\x9ff\x1c\xa7F\x9bb\x8b\xe5\xde\xd8\x07\xa0\x91B\xfaf\x9d\xe9\x8f\r\x9d6\x86\x94\x1c!\xd5\xab\xb2a\xc6\xa5I\x1a\xf95)\xe56\xd1KBmQLh4`\x97\xd4\xf7+\x8b\x9faYR\xe2:4H6X>1\xf3\x9a)\xaf\x19\xba_\x95\xe7D\x0bE(\xb3<\xbd\x03\xce\x04\x125\x02\xd7\x120\xb2\x8d\xbfJi\x8clFPI.\x95\x85L\xb6\xef\xb24\x9b\x8e`8{(\xcb\xba\xbe=p\xe5\xd6>\x99\xddS\x9c\xde\xc2\xedQF\xd7\x8a\x90\xa4\x975\xb0\x1c\xf2\xc5\x880\xbd\xee\xa2@\x9ee\xd7>\xd2\xa0f\xdc\x8e,Z%\x17\x8c\x16\xbf\xfd\xf5\xb1!\x0b\xfcS\xd9]SK\xd5\xa4\x9fY\xa5\xa4\x96\xb5I\xbb\xe0\xda\x10e>\xb8\xe2\xb4Q\xbf\xde\xc4\xf07#@A{\xe6\x90\xe9\xe6\xb0\xdc\xc4?T\x11\xe7\xcc\xbb\x95\xf4p\xba\x04+]\xfc\xe2\xf7\xc5~\xc9N}/\xdb\x8a\x1e\xd9\xf7w6\xc7\xc4\xba(\xd3-\';\xbb\x8e\xaeOI\xc9e\xf5d\xcd\xb1\x94\xda\x1fGH\x12\'\x1e\xe7\xb6\xab7l\xd0\xb3\\JN\xe7\xfb\xddg\xeb\x80\xf1\x9d\x1f\xe5U\x85b%\x83\x80\x15A8\x829B\x95\xf7p\x1aN\xc7\xf7XU\x8e\xf6\x01\xa4\x15\'Z\x0b\xd2`\xb1t\xbb\xce\xf1~Y\xc2"I\'\x84E\xf2\xde@X\xa4\xca\x13\x16i\xeb\x08\xfb\xf7\x80E\x92\x8e\x01\x8b\xdc\x9d\x07,\xcc\t\xfa\xb1o(\xa9\x0c[{\xe9n\xa5f~i\x14r\xe2\x8cnyd\xeb\x96\xe5Ht\x90c\xe5D\xc7\x1dA\xf4\x1e\xd2 \xd4?\xa9B\x1d`?\xafB\xdd\x94\xd7\x0c\xbd(#H\xddy\xca\x08\xad\xdd\xf9\x16FB\xc4\xc0H\x88rIFB\xf4\x13FB\xa2\x17\x18\ts\xce\x8bP\xf67"\x94\x9d\x11\xa1\xec\x05\x11\xa2\x95;\xffQ\x84f\xfe\xf8\x7fE\xa8#I\x90u\xc2\x04\xc5\xed\xf3\x9f\xfd\xe1&\xfa\x8fT)\x92uB\\$\xf1\r\xc4E\xca<q\x91\xbe\x0b\x12\x17\xd1:&.\x82x\x9e\xb80\xe7\x02\xaa\xc4D\xbb2\xdd\x8bt`c\xdcG\xf0\xdc\xdbcP\xaf<O\xef\x82|\xc55#mk\x9bH\x84}Y\x8d\x88\x1c\xa2\r\xd9KL\x1cT\x93,\xa9:[Q\x9fV\x88\xb8\xbe\xf6\x1d\xf7\xd2\xb5\xff\x00\t\xac*z"""
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
style_str = zlib.decompress(style_str_zip)[1:]
# Uncomment next line to see css
# print style_str

def just(string, type, n):
	'''Justify a string to length n according to type.'''
	if type == '::':
		return string.center(n)
	elif type == '-:':
		return string.rjust(n)
	elif type == ':-':
		return string.ljust(n)
	else:
		return string

def normtable(text):
	'''Aligns the vertical bars in a text table.'''
	# Start by turning the text into a list of lines.
	lines = text.splitlines()
	rows = len(lines)
	
	# Figure out the cell formatting.
	# First, find the separator line.
	for i in range(rows):
		if set(lines[i]).issubset('|:.-'):
			formatline = lines[i]
			formatrow = i
			break
	# Delete the separator line from the content.
	del lines[formatrow]
	
	# Determine how each column is to be justified.
	formatline = formatline.strip(' ')
	if formatline[0] == '|': formatline = formatline[1:]
	if formatline[-1] == '|': formatline = formatline[:-1]
	fstrings = formatline.split('|')
	justify = []
	
	for cell in fstrings:
		ends = cell[0] + cell[-1]
		if ends == '::':
			justify.append('::')
		elif ends == '-:':
			justify.append('-:')
		else:
			justify.append(':-')
	# Assume the number of columns in the separator line is the number
	# for the entire table.
	columns = len(justify)
	# Extract the content into a matrix.
	content = []
	
	for line in lines:
		line = line.strip(' ')
		if line[0] == '|': line = line[1:]
		if line[-1] == '|': line = line[:-1]
		cells = line.split('|')
		# Put exactly one space at each end as "bumpers."
		linecontent = [ ' ' + x.strip() + ' ' for x in cells ]
		content.append(linecontent)
	# Append cells to rows that don't have enough.
	rows = len(content)
	
	for i in range(rows):
		while len(content[i]) < columns:
			content[i].append('')
	# Get the width of the content in each column. The minimum width will
	# be 2, because that's the shortest length of a formatting string and
	# because that matches an empty column with "bumper" spaces.
	widths = [2] * columns
	
	for row in content:
		for i in range(columns):
			widths[i] = max(len(row[i]), widths[i])
	# Add whitespace to make all the columns the same width and 
	formatted = []
	
	for row in content:
		formatted.append('|' + '|'.join([ just(s, t, n) for (s, t, n) 
		                                 in zip(row, justify, 
		                                        widths) ]) + '|')
	# Recreate the format line with the appropriate column widths.
	formatline = '|' + '|'.join([ s[0] + '-'*(n-2) + s[-1] for (s, n) 
	                             in zip(justify, widths) ]) + '|'
	# Insert the formatline back into the table.
	formatted.insert(formatrow, formatline)
	# Return the formatted table.
	return '\n'.join(formatted)

#-------------------------------------------------------------------------
def make_form(nrows, ncols):
	'''Construct form using bs4'''
	soup = BeautifulSoup()
	h2 = soup.new_tag('h2')
	h2.append('Multimarkdown table generator')
	soup.find('body').append(h2)
	form = soup.new_tag('form', method='post')
	# We cannot use class in new_tag, so we do:
	form['class']='mtable'
	soup.find('body').append(form)
	# Make new list
	ul = soup.new_tag('ul')
	form.append(ul)
	style = soup.new_tag('style', type='text/css')
	style.append(style_str)
	soup.find('head').append(style)
	
	for j in range(nrows + 2):
		if j == 0:
			li = soup.new_tag('li', str(j))
			ul.append(li)
			# Generate options strings
			opt_str = ['Left', 'Center', 'Right']	
			# Append selectors to first row
			for i in range(ncols):
				sel = soup.new_tag('select', 
				                   id='sel'+str(i))
				sel['class'] = 'select'
				sel['name'] = 'sel' + str(i)
				opts = []	
				# Generate options, we need to generate new opt object
				# otherwise opts will be moved from one selector to another
				for k in range(len(opt_str)):
					opt = soup.new_tag('option', value=opt_str[k])
					opt.append(opt_str[k])
					opts.append(opt)
					# Append options to selects
					sel.append(opts[k])	
				li.append(sel)	
		# Now, let's add headers		
		elif j == 1:
			li = soup.new_tag('li', str(j))
			ul.append(li)
			for i in range(ncols):
				input = soup.new_tag('input', 
				                     type='text', 
				                     id='hdr'+str(i))
				input['class'] = 'input-hdr'
				input['name']= 'hdr' + str(i)
				li.append(input)
		else:
			li = soup.new_tag('li', str(j))
			ul.append(li)
			for i in range(ncols):
				input = soup.new_tag('input', 
				                     type='text', 
				                     id='inp' + str(j-2) + str(i))
				input['class'] = 'input'
				input['name']= 'inp' + str(j-2) + str(i)
				li.append(input)			
	
	# Container for buttons		
	divb = soup.new_tag('div')
	divb['class'] = 'div'
	form.append(divb)	
	
	submit_btn = soup.new_tag('input', type='submit')	
	submit_btn['class'] = 'submit'
	submit_btn['name'] = 'submit'
	submit_btn['value'] = 'Generate Table'
	
	divb.append(submit_btn)	
	# Container for messages
	divm = soup.new_tag('div', id='divm')
	divm['class'] = 'div'
	soup.find('body').append(divm)
	pre = soup.new_tag('pre')		
	code = soup.new_tag('code', id='code')
	code.append('Press Generate Table button. Generated code will be placed in the clipboard.')
	pre.append(code)
	divm.append(pre)

	return soup.prettify()
	
#-------------------------------------------------------------------------
def make_table(fmts, hdrs, vals):
	'''Produce multimarkdown table from python lists of formats, headers,
	and values.
	'''
	# Replace empty headers
	hdrs = [' ' if hdr is None else hdr for hdr in hdrs]
	headers = '|' + '|'.join(hdrs) + '|' + '\n'
	# Construct format list
	fmts_mmd = []
	
	for fmt in fmts:
		if fmt == 'Left':
			fmts_mmd.append(':-')
		elif fmt == 'Right':
			fmts_mmd.append('-:')
		else:
			fmts_mmd.append(':-:')
	
	formats = '|' + '|'.join(fmts_mmd) + '|' + '\n'
	# Replace Nones with empty strings
	nrows = len(vals)
	ncols = len(vals[0])
	values = ''
	
	for i in range(nrows):
		for j in range(ncols):
			if vals[i][j] == None:
				vals[i][j] = ''
		values += '|' + '|'.join(vals[i]) + '|' + '\n'	
	
	table = normtable(headers + formats + values)
	clipboard.set(table)
	
	return table

#-------------------------------------------------------------------------
class RequestHandler(BaseHTTPRequestHandler):
	# We need to pass parameters, but we don't want to instantiate 
	# the class, so we do:
	@classmethod
	def setParams(self, nrows, ncols, html):
		self.html = html
		self.nrows = nrows
		self.ncols = ncols
		self.soup = BeautifulSoup(html)
		
	def do_GET(self):  #load initial page
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		self.wfile.write(self.html)
		
	def do_POST(self):  #process requests
		form = cgi.FieldStorage(fp = self.rfile, 
		                        headers = self.headers, 
		                        environ = 
		                        {'REQUEST_METHOD':'POST','CONTENT_TYPE':
		                                   self.headers['Content-Type']})
		
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		frmt, hdrs, vals = self.getVals(form)
		msg = make_table(frmt, hdrs, vals)
		self.html = self.printMsg('Your code is:\n\n' + msg)
		self.wfile.write(self.html)
		
	def getVals(self, form):
		'''Retun html with current values.'''
		frmt = []
		hdrs = []
		vals = []
		# Get values from selects first
		for i in range(self.ncols):
			name = 'sel'+ str(i)
			val = form.getfirst(name)
			sel = self.soup.find('select', id=name)
			opt = sel.findChild('option', value=val)
			opt['selected']='selected'
			frmt.append(val)
			
		# Get headers
		for i in range(self.ncols):
			name = 'hdr' + str(i)
			val = form.getfirst(name)
			hdr = self.soup.find('input', id=name)
			hdr['value'] = val
			hdrs.append(val)
			
		# Get the rest
		for j in range(self.nrows):
			vals_row = []
			for i in range(self.ncols):
				name = 'inp' + str(j) + str(i)
				val = form.getfirst(name)
				inp = self.soup.find('input', id=name)
				inp['value'] = val
				vals_row.append(val)
			vals.append(vals_row)
		
		return (frmt, hdrs, vals)
				
	
	def printMsg(self, msg):
		'''Output in the html.'''
		soup = BeautifulSoup(self.html)
		code = self.soup.find('code', id='code')
		code_n = self.soup.new_tag('code', id='code')
		code_n.append(msg)
		code.replace_with(code_n)
		
		return self.soup.prettify()


def _validate_input(row=True):
	'''Helper function to validate input.'''
	msg1 = 'Enter number of %s: '
	msg2 = '***Error: Number of %s cannot be negative or exceed %d'
	
	if row == True:
		msg1 = msg1 % ('rows')
		msg2 = msg2 % ('rows', MAX_DIM)
	else:
		msg1 = msg1 % ('columns')
		msg2 = msg2 % ('columns', MAX_DIM)
		
	par = raw_input(msg1)
	
	try:
		par = int(par)
		if par < 1 or par > MAX_DIM:
			print(msg2)
			par = _validate_input(row)
	except ValueError:
		# Cannot convert to int
		print('***Error: Enter a number between 1 and %d' % (MAX_DIM))
		par = _validate_input(row)
	
	return par
				
#-------------------------------------------------------------------------
if __name__ == '__main__':
	
	nrows = _validate_input(True)
	ncols = _validate_input(False)
	html = make_form(nrows, ncols)
	RequestHandler.setParams(nrows, ncols, html)
	server = HTTPServer(('', 80), RequestHandler)
	webbrowser.open('http://localhost', stop_when_done=True)
	
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		sys.exit(0)
		
	
	
	