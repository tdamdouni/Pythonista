# coding: utf-8

'''This script generates the words_en.data file from the Letterpress dictionary. The list of words is simply converted to a set and then serialized using the marshal module (which is faster than pickle).'''

import urllib
import marshal
words = set()
f = urllib.urlopen('https://github.com/atebits/Words/blob/master/Words/en.txt?raw=true')
for line in f:
	words.add(line.strip())
with open('words_en.data', 'w') as out:
	marshal.dump(words, out)