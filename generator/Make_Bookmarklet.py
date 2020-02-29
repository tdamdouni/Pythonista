# coding: utf-8

# http://unapologetic.io/posts/2014/01/28/javascript-bookmarklet-builder-on-ios/

from __future__ import print_function
import sys
import re
import clipboard
import urllib

if len(sys.argv) > 1:
	source_code = sys.argv[1]
else:
	source_code = ''' [YOUR CODE HERE] '''

split_code = source_code.split('\n') # Split code at newlines

# Remove first line if it is already a bookmarklet
if '// javascript:' in split_code[0]:
    split_code.pop(0)

source_code = '\n'.join(split_code) # Rejoin lines of source code without bookmarklet line (if it was present)

# Strip line-ending and line-leading whitespace
for i in range(len(split_code)):
    split_code[i] = split_code[i].rstrip()
    split_code[i] = split_code[i].lstrip()

bookmarklet = ''.join(split_code) # Rejoin code as bookmarklet with newlines removed
bookmarklet = re.sub(re.compile("//.*?\n" ) ,"" ,bookmarklet) # Kill commented lines
bookmarklet = re.sub(re.compile('/\*.*?\*/',re.DOTALL ) ,'' ,bookmarklet) # Kill block comments
bookmarklet = re.sub('\s\s+', ' ', bookmarklet) # Space runs to single spaces, tabs to spaces

# UTF-8 encode and URL escape
bookmarklet = bookmarklet.encode('utf-8')
bookmarklet = urllib.quote(bookmarklet, safe='=;()+?!')

bookmarklet = 'javascript:' + bookmarklet # Append 'javascript:' before bookmarklet

print('// ' + bookmarklet + '\n' + source_code) # Print full source code with new bookmarklet as commented first line
clipboard.set(bookmarklet) # Put bookmarklet on clipboard