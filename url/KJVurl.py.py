# KJVurl.py
# convert a list of verse citations, one to a line in the form 'Judges 2:2' into markdown formatted links to the corresponding verse in an online service
# this example depends on a correspondence of the url to the verse by simple substitution of a hyphen for each blank or colon
# for iOS7 pythonista, due to reliance on clipboard module

import re
import clipboard

# site whose citation scheme will be usef
baseref = "http://www.kingjamesbibleonline.org/"
# convenience definitions
blankspace = ' '
separator = '-' # baseref dependent
leftbracket = '['
rightbracket = ']'
colon = ':'
nl = '\n'

# read in citation list
input = [clipboard.get()]
# create a list object with verses to be matched to urls
verses = input[0].split(nl)

# function to read a list and format each element
def link_verse(verselist):
	results = []
	for verse in verselist:
		if verse != '':
			cite = verse.replace(blankspace, separator)
			cite = cite.replace(colon, separator)
			results.append(leftbracket)
			results.append(verse)
			results.append(rightbracket)
			results.append(nl)
			results.append(leftbracket)
			results.append(verse)
			results.append(rightbracket)
			results.append(colon)
			results.append(blankspace)
			results.append(baseref)
			results.append(cite)
			results.append(nl)
	return results,
	
# convert list of verses into markdown links
# to corresponding webpage
versified = link_verse(verses)

results_list = []

# collect the results into a string
for verse in versified:
	results_list.append(''.join(verse))
	
# copy to the system clipboard
clipboard.set(''.join(results_list))

