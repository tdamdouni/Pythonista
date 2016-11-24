# https://gist.github.com/paultopia/a0385f1cf619022c587e

# assumes documents are provided in the form of a list of (docid, doctext) tuples named thedocslist. docid = int/string/float; doctext = string

import nltk
import string
from collections import Counter

# get rid of punctuation, numbers; make all lowercase.  no stemming.

counterslist = []
for onedocument in thedocslist:
	cleanstring = onedocument[1].translate(string.maketrans("",""), string.punctuation)
	cleanstring = cleanstring.translate(string.maketrans("",""), string.digits)
	cleanstring = filter(lambda x: x in string.printable, cleanstring)
	wordlist = [i.lower() for i in cleanstring.split()]
	ctupe = (onedocument[0], Counter(wordlist))
	counterslist.append(ctupe)
	
justcounters = [x[1] for x in counterslist]
totalcounter = reduce(lambda a, b: a+b, justcounters)

def wordstring(atupe):
	return "%s: %s" % (atupe[0], atupe[1])
	
	
def makestring(onecounter):
	firstline = "Document ID: " + str(onecounter[0]) + "\n"
	morelineslist = [wordstring(listitem) for listitem in onecounter[1].most_common()]
	linestring = '\n'.join(morelineslist)
	return firstline + linestring
	
bigstring = '\n\n'.join([makestring(i) for i in counterslist])
mainstring = makestring(("TOTAL", totalcounter))
totalstring = bigstring + '\n\n' + mainstring

with open("wordlist.txt", 'w') as wordfile:
	wordfile.write(totalstring)

