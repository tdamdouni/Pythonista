# coding: utf-8

# @omz

# https://gist.github.com/omz/e141f676504b743dbaa8

from __future__ import print_function
from objc_util import ObjCClass
UITextChecker = ObjCClass('UITextChecker')

def check_word(word, lang='en_US'):
	c = UITextChecker.new().autorelease()
	check = c.rangeOfMisspelledWordInString_range_startingAt_wrap_language_
	misspelled_range = check(word, (0, len(word)), 0, False, lang)
	return (misspelled_range.location != 0)
	
test_words = ['foo', 'bar', 'baz', 'quuz', 'cat', 'dog']
for word in test_words:
	print('%s: %s' % (word, check_word(word)))

