# -*- coding: utf-8 -*-

# https://gist.github.com/technocrat/5486147

"""
replacer.py: 
2013-04-29
(c) 2013 Richard Careaga, all rights reserved.
Subject to license terms and conditions at
http://richard-careaga.com/lic2013.txt
 
install this script to your pythonista.app top-level directory

use cases: process texts from apps that lack search/replace or TextExpander

todo: handle capitalization 

"""

import re

# dictionary of keys:values for substitutions -- could be kept
# in a separate file for import

# paste in or clipboard.get() for your substitutions

# example

D = {'ipsum': ['FOO'], 'commodo':['BAR'], 'laborum':['BAZ']}

# text to be processed
# paste in or clipboard.get() for yours

# example

s = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

# tokenize words and punctuation into a list

t = re.split('(\W+)',  s) 

# create an empty list to hold intermediate results

b = []

# iterate over list, if a list element is in the dictionary, append
# the substitute; otherwise, send the element

for word in t:
    if word in D:
        b.append(D[word][0])
    else:
        b.append(word)

# reconstruct the string

r = ''.join(b)

# result
"""
'Lorem FOO dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea BAR consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est BAZ.'
"""

# show result

print(r)

