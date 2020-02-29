# coding: utf-8

# https://forum.omz-software.com/topic/2480/encryption-list-ranges-and-python/2

from __future__ import print_function
extra_chars  = ["?","!",".",",","_"," "]

# 2 steps
x = [(chr(ind + 32), chr(ind)) for ind in range(65,91)]
y = [tp for tupl in x for tp in tupl]
char_list1 = y + extra_chars
print(char_list1, '\n')

# 1 step
char_list2 = [tp for tupl in
            [(chr(ind + 32), chr(ind)) for ind in range(65,91)]
                for tp in tupl] + extra_chars


print(char_list2)