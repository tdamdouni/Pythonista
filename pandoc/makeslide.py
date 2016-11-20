# https://gist.github.com/paultopia/0c57899407aed81f6932

import argparse

# this first bit is to enable multiline help text.  apparently this is a known problem with argparse.
# Solution jacked from http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text

import textwrap as _textwrap
class MultilineFormatter(argparse.HelpFormatter):
	def _fill_text(self, text, width, indent):
		text = self._whitespace_matcher.sub(' ', text).strip()
		paragraphs = text.split('|n ')
		multiline_text = ''
		for paragraph in paragraphs:
			formatted_paragraph = _textwrap.fill(paragraph, width, initial_indent=indent, subsequent_indent=indent) + '\n\n'
			multiline_text = multiline_text + formatted_paragraph
		return multiline_text
		
parser = argparse.ArgumentParser(description="""This is a utility to make a reveal.js slideshow from a markdown file given the template at:
                                            |n
                                            http://gist.github.com/paultopia/0c57899407aed81f6932
                                            |n
                                            Commandline flags and such are given below.  In addition, the following arguments are valid:
                                            |n
                                            Themes: black, white, league (default), sky, beige, simple, serif, blood, night, moon, solarized
                                            |n
                                            Transitions: none (default), fade, slide, convex, concave, zoom
                                            """, formatter_class=MultilineFormatter)
parser.add_argument("infile", help="the markdown file containing the slideshow")
parser.add_argument("-t", "--theme", nargs='?', default="league", help="name of theme")
parser.add_argument("-r", "--transition", nargs='?', default="none", help="name of transition")
parser.add_argument("-o", "--outfile", nargs='?', default=" ", help="filename of outfile")
parser.add_argument("-u", "--unsafe", action="store_true", help="UNSAFE mode: overwrite output file. Off by default.")
args = parser.parse_args()


from os.path import isfile

print(' ')
print(' ')
print("CONVERTING MARKDOWN FILE TO REVEAL JS SLIDES USING PANDOC")

# validate input file
if args.infile[-3:] != '.md':
	print(' ')
	print("You gave me an input filename without a .md extension.  Appending to file.")
	theinfile = args.infile + '.md'
else:
	theinfile = args.infile
if not isfile(theinfile):
	raise IOError("input %s file not found" % theinfile)
	
# validate output file
if args.outfile == ' ':
	print(' ')
	print("You didn't give me an output filename.  Using input filename with extension changed to html.")
	theoutfile = theinfile[0:-3] + '.html'
elif args.outfile[-5:] != '.html':
	print(' ')
	print("You gave me an output filename without a .html extension.  Appending to file.")
	theoutfile = args.outfile + '.html'
	
else:
	theoutfile = args.outfile
	
def lazyiter():
	number = 0
	while True:
		yield number
		number += 1
mycounter = lazyiter()

# prevent overwriting of output file
if not args.unsafe:
	while isfile(theoutfile):
		print(' ')
		print("You gave me an output file (%s) that already exists.  Appending a number to the front to avoid overwriting." % theoutfile)
		theoutfile = str(next(mycounter)) + theoutfile
		print(' ')
		print('New file is: %s' % theoutfile)
		
# check and validate themes and transitions
validthemes = ["black", "white", "league", "sky", "beige", "simple", "serif", "blood", "night", "moon", "solarized"]
validtransitions = ["none", "fade", "slide", "convex", "concave", "zoom"]
thetheme = args.theme.lower()
thetransition = args.transition.lower()
if thetheme not in validthemes:
	raise ValueError("No theme called %s found.  Valid themes are: %s." % (thetheme, ', '.join(validthemes)))
if thetransition not in validtransitions:
	raise ValueError("No theme called %s found.  Valid themes are: %s." % (thetransition, ', '.join(validtransitions)))
	
	
commandstring = 'pandoc -t html5 --template=revealjs.html --standalone --section-divs --variable theme="%s"  --variable transition="%s" %s -o %s' % (thetheme, thetransition, theinfile, theoutfile)
print(' ')
print('Converting %s to %s using theme %s and transition %s.' % (theinfile, theoutfile, thetheme, thetransition))
print(' ')
print(' ')
from subprocess import call
call(commandstring, shell=True)

