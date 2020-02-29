# coding: utf-8

# @omz

# https://gist.github.com/omz/599ef8aeae22620261c6

'''
Demo of using the built-in iOS dictionary to check words

NOTES: This is quite slow, it might be possible to use the spell-checking
      dictionary for this instead, haven't tried that yet.
      If no dictionary is downloaded yet, the API will always return True
      (probably so that the "Define" menu item can be shown before
      a dictionary has been downloaded).
'''
from __future__ import print_function

from objc_util import ObjCClass

def is_word_valid(word):
	reflib = ObjCClass('UIReferenceLibraryViewController')
	return reflib.dictionaryHasDefinitionForTerm_(word)
	
test_words = ['foo', 'bar', 'quuz', 'cat', 'dog']
for word in test_words:
	print('%s: %s' % (word, is_word_valid(word)))

