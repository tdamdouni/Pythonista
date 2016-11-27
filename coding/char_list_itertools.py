# coding: utf-8

# https://forum.omz-software.com/topic/2480/encryption-list-ranges-and-python/3

import itertools, string

char_list2 = list(itertools.chain(*zip(string.ascii_lowercase, string.ascii_uppercase)))
print(char_list2)

import string

char_list2 = []
for i in xrange(len(string.ascii_lowercase)):
    char_list2.append(string.ascii_lowercase[i])
    char_list2.append(string.ascii_uppercase[i])
print(char_list2)

import itertools

char_list3 = list(itertools.chain(*zip(string.ascii_lowercase, string.ascii_uppercase)))
print(char_list3)