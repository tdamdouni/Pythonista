#!/usr/bin/env python3

# https://gist.github.com/reagle/2eb0fdd33951456e69bbb32e9e422da9

# -*- coding: utf-8 -*-
# (c) Copyright 2016 by Joseph Reagle
# Licensed under the GPLv3, see <http://www.gnu.org/licenses/gpl-3.0.html>
#
"""Pretty print a markdown file as source"""

import io
import logging
import markup   # http://markup.sourceforge.net/#documentation
from markup import oneliner as o
import os
from os import chdir, environ, mkdir, rename
from os.path import abspath, basename, dirname, expanduser, \
    isfile, realpath, splitext
import re
import webbrowser


HOME = environ['HOME']
TMP_DIR = environ['TMPDIR']
# BROWSER = os.environ['BROWSER'] if 'BROWSER' in os.environ else None

critical = logging.critical
info = logging.info
dbg = logging.debug
warn = logging.warn
error = logging.error
excpt = logging.exception

# Main ####################################


def process(args, filename):

	info("filename = %s" % filename)
	assert isfile(filename)
	base_name = basename(filename)
	bald_name = splitext(base_name)[0]
	# output_dir = dirname(realpath(filename))
	output_dir = TMP_DIR
	info("base_name = %s" % base_name)
	info("bald_name = %s" % bald_name)
	info("output_dir = %s" % output_dir)
	html_fn = os.path.join(output_dir, bald_name + '-pp.html')
	info('output_dir = %s; html_fn = %s' % (output_dir, html_fn))
	
	with io.open(filename, 'r', encoding='utf8') as f:
		lines = f.readlines()
		
	page = markup.page()
	page.init(title=lines[0],
	css=('http://reagle.org/joseph/2016/06/md-pp.css'),
	charset='utf-8')
	
	margin_markup = re.compile(r'(^[#>:]+)(.*)')
	for line_no, line in enumerate(lines):
		line = line.replace('<!--', '&lt;!--')
		line = line.replace('-->', '--&gt;')
		if not line.strip():                    # empty line
			page.p(('&nbsp;'))
		elif margin_markup.match(line):
			token = margin_markup.match(line).group(1)
			if token.startswith('#'):
				if len(token) == 2:
					page.h1(line)
				elif len(token) == 3:
					page.h2(line)
				elif len(token) == 4:
					page.h3(line)
				else:
					page.h4(line)
			elif token.startswith('>'):
				page.blockquote(line, class_="quote")
			elif token.startswith('  '):
				page.blockquote(line, class_="indent")
			elif token.startswith(':'):
				page.blockquote(line, class_="definition")
				
		else:
			page.p.open()
			page.span(line_no, class_="line_no")
			page.span(line, class_="prose")
			page.p.close()
			
	with io.open(html_fn, 'w', encoding='utf8') as f:
		f.write(str(page))
		
	webbrowser.open('file://' + html_fn)
	
if '__main__' == __name__:

	import argparse  # http://docs.python.org/dev/library/argparse.html
	arg_parser = argparse.ArgumentParser(description='Pretty print a markdown file as source')
	
	# positional arguments
	arg_parser.add_argument('files', nargs=1, metavar='FILE')
	# optional arguments
	arg_parser.add_argument('-L', '--log-to-file',
	action="store_true", default=False,
	help="log to file %(prog)s.log")
	arg_parser.add_argument('-V', '--verbose', action='count', default=0,
	help="Increase verbosity (specify multiple times for more)")
	arg_parser.add_argument('--version', action='version', version='0.1')
	args = arg_parser.parse_args()
	
	log_level = 100  # default
	if args.verbose == 1: log_level = logging.CRITICAL  #50
	elif args.verbose == 2: log_level = logging.INFO    #20
	elif args.verbose >= 3: log_level = logging.DEBUG   #10
	LOG_FORMAT = "%(levelno)s %(funcName).5s: %(message)s"
	if args.log_to_file:
		logging.basicConfig(filename='md-pp.log', filemode='w',
		level=log_level, format=LOG_FORMAT)
	else:
		logging.basicConfig(level=log_level, format=LOG_FORMAT)
		
	process(args, args.files[0])

