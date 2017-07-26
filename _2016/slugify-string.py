# http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename

def slugify(value):
	"""
	Normalizes string, converts to lowercase, removes non-alpha characters,
	and converts spaces to hyphens.
	"""
	import unicodedata
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
	value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
	value = unicode(re.sub('[-\s]+', '-', value))

# ---

import string
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
valid_chars
'-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
filename = "This Is a (valid) - filename%$&$ .txt"
''.join(c for c in filename if c in valid_chars)
'This Is a (valid) - filename .txt'

# ---

import base64
file_name_string = base64.urlsafe_b64encode(your_string)

# ---

import unicodedata

validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)

def removeDisallowedFilenameChars(filename):
	cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
	return ''.join(c for c in cleanedFilename if c in validFilenameChars)

# ---

import re
badchars= re.compile(r'[^A-Za-z0-9_. ]+|^\.|\.$|^ | $|^$')
badnames= re.compile(r'(aux|com[1-9]|con|lpt[1-9]|prn)(\.|$)')

def makeName(s):
	name= badchars.sub('_', s)
	if badnames.match(name):
		name= '_'+name
	return name

# ---

import re

str = "File!name?.txt"
f = open(os.path.join("/tmp", re.sub('[^-a-zA-Z0-9_.() ]+', '', str))

# ---

valid_file_name = re.sub('[^\w_.)( -]', '', any_string)

# ---

import re
t = re.compile("[a-zA-Z0-9.,_-]")
unsafe = "abc∂éåß®∆˚˙©¬ñ√ƒµ©∆∫ø"
safe = [ch for ch in unsafe if t.match(ch)]

# ---

from random import choice
from string import ascii_lowercase, ascii_uppercase, digits
allowed_chr = ascii_lowercase + ascii_uppercase + digits

safe = ''.join([choice(allowed_chr) for _ in range(16)])
# => 'CYQ4JDKE9JfcRzAZ'

# ---

import string
for chr in your_string:
	if chr == ' ':
		your_string = your_string.replace(' ', '_')
	elif chr not in string.ascii_letters or chr not in string.digits:
		your_string = your_string.replace(chr, '')
