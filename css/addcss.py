from __future__ import print_function
# https://gist.github.com/paultopia/e61d63cc58cecc36e3b1

# Easy way to add CSS or whatever to header of a bunch of HTML files at once.

# USAGE:
#
# To add code to the end of every <head> tag (like a css link, a font link, etc.) to quick-format an entire website:
# 1.  Start in the top-level-directory of the site.  Put this file there.
# 2. Add your formtting for the <head> tag  to the formatme variable.
#           EXAMPLE: mine was '<link href="https://fonts.googleapis.com/css?family=Halant:300" rel="stylesheet" type="text/css"><link rel="stylesheet" href="http://paul-gowder.com/conlawII/prettify.css">'
#           be sure to either escape quotes or use single quotes to demarcate the string and double-quotes in the html/vice versa
# 3.  Run this script.
# 4. Bam.  Every html page in in the top-level directory and all its subdirectories now has the formatting you want.

formatme = 'YOUR STRING HERE'
newstring = formatme + '</head>'
import re, os

def peek(filename):
	with open(filename) as thefile:
		return (formatme not in thefile.read()) and filename[-4:] == 'html'
		
def addcss(filename):
	with open(filename) as thefile:
		thepage = thefile.read()
	newpage = re.sub('</head>', newstring, thepage)
	with open(filename, 'w') as thefile:
		thefile.write(newpage)
		
rootDir = os.getcwd()
for dirpath, dirnames, filenames in os.walk(rootDir):
	for fname in filenames:
		if peek(os.path.join(dirpath, fname)):
			addcss(os.path.join(dirpath, fname))
			print('Added to: ' + fname)

