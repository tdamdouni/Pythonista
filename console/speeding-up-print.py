# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/2909/suggestion-speeding-up-print

# In general, I would recommend trying to minimize the number of individual pieces of text that are printed. For example, print 'foo ' + 'bar' is faster than print foo, bar because in the latter case, the two arguments are printed individually, which is generally more expensive. Also, in cases where you want to print several lines, consider joining them, e.g.:

# Pretty slow:
from __future__ import print_function
for line in some_list:
	print(line)
# Faster:
print('\n'.join(some_list))

