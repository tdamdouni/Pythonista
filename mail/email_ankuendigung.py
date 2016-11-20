#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""Format announcement of next user group meeting given a template and a data
file and open an email client with recipient, subject and body pre-filled.

Usage:

    ankuendigung.py ankuedigung.tmpl meeting.data

where ``ankuendigung.tmpl`` is a Jinja2 template and ``meeting.data`` is an
INI-style configuration file with the meeting data in the following format::

    [general]
    subject = ANN: nächstes Treffen der pyCologne am %s Uhr
    greeting = Hallo,
    salutation = Grüße,
    sender = Joe Doe

    [meeting]
    date = 2014-08-13 19:00
    address = Chaos-Computer-Club, Köln-Ehrenfeld, Heliosstraße 6a

    [agenda]
    1: How to train your Python;Zen van Koda
    2: Python 25k Diskussion;Alle
    ...

"""

from __future__ import print_function

import locale
import sys
import subprocess

try:
	from ConfigParser import RawConfigParser
except ImportError:
	from configparser import RawConfigParser
	
from datetime import datetime
from os.path import basename, dirname

from jinja2 import FileSystemLoader, Environment

if hasattr(str, 'decode'):
	def decode(s, enc):
		return s.decode(enc)
else:
	def decode(s, enc):
		return s
		
def load_data(fn):
	"""Load meeting data from INI-style data file."""
	parser = RawConfigParser()
	parser.read(fn)
	data = {}
	for section in ('general', 'meeting'):
		if parser.has_section(section):
			data.update(dict((k, decode(v, 'utf-8'))
			for k,v in parser.items(section)))
	data['date'] = datetime.strptime(data['date'], '%Y-%m-%d %H:%M')
	data['agenda'] = [decode(parser.get('agenda', o), 'utf-8').split(';')
	for o in sorted(parser.options('agenda'))]
	return data
	
def render_from_template(directory, template_name, **kwargs):
	"""Render named Jinja2 template in given direcctory."""
	loader = FileSystemLoader(directory)
	env = Environment(loader=loader)
	template = env.get_template(template_name)
	return template.render(**kwargs)
	
def main(args=None):
	try:
		template = args[0]
		data = load_data(args[1])
	except IndexError:
		print("Usage: %s TEMPLATE DATAFILE" % basename(sys.argv[0]))
		return 2
		
	mail = render_from_template(dirname(template), basename(template), **data)
	subject = data['subject'] % (data['date'].strftime('%d.%m.%y %H:%M'),)
	subprocess.call(['xdg-email', '--utf8', '--subject', subject, '--body',
	mail.encode('utf-8'), 'mailto:' + data['recipient']])
	
if __name__ == '__main__':
	locale.setlocale(locale.LC_ALL, '')
	main(sys.argv[1:])

