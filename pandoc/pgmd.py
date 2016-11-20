import argparse

parser = argparse.ArgumentParser(description="Quick and easy commandline wrapper for converting markdown to word, html, and pdf formats.")
parser.add_argument("infile", help="the markdown file containing the document")
parser.add_argument("type", help="the type of output: html, word, or pdf")
parser.add_argument("-o", "--outfile", nargs='?', default=" ", help="filename of outfile (optional, will use same name as infile with new extension otherwise)")
parser.add_argument("-u", "--unsafe", action="store_true", help="UNSAFE mode: overwrite output file. Off by default, will append numbers to front of duplicates.")
parser.add_argument("-a", "--append", nargs='?', default=" ", help="Optional file to append to header file, for HTML (to add CSS or JS). Ignored otherwise.")
args = parser.parse_args()

validtypes = ['html', 'word', 'pdf']
outputtype = args.type.lower()
if outputtype not in validtypes:
    raise ValueError("No output type called %s found.  Valid output types are are: %s." % (outputtype, ', '.join(validtypes)))

from os.path import isfile

print(' ')
print(' ')
print("CONVERTING MARKDOWN FILE TO %s USING PANDOC" % outputtype.upper())

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
    print("You didn't give me an output filename.  Using input filename with extension changed to appropriate type.")
    if outputtype != 'word':
        theoutfile = theinfile[0:-3] + '.' + outputtype
    else:
        theoutfile = theinfile[0:-3] + '.docx'
elif (args.outfile[-5:] != '.html') and (outputtype == "html"):
    print(' ')
    print("You gave me an output filename without a .html extension.  Appending to file.")
    theoutfile = args.outfile + '.html'
elif (args.outfile[-5:] != '.docx') and (outputtype == "word"):
    print(' ')
    print("You gave me an output filename without a .docx extension.  Appending to file.")
    theoutfile = args.outfile + '.docx'
elif (args.outfile[-4:] != '.pdf') and (outputtype == "pdf"):
    print(' ')
    print("You gave me an output filename without a .pdf extension.  Appending to file.")
    theoutfile = args.outfile + '.docx'
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


if (outputtype == "html") and (args.append != ' '):
    commandstring = 'pandoc -s -H %s %s -o %s' % (args.append, theinfile, theoutfile)
else:
    commandstring = 'pandoc -s %s -o %s' % (theinfile, theoutfile)
print(' ')
print('Converting %s to %s in %s format' % (theinfile, theoutfile, outputtype))
print(' ')
print(' ')
from subprocess import call
call(commandstring, shell=True)
