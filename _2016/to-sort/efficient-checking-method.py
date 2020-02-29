# coding: utf-8

# https://forum.omz-software.com/topic/2653/efficient-checking-method

from __future__ import print_function
nums_list = []
for number in range(1000): # This makes a list with a ton of uneven numbers.
    eoro_check = (number-1)%2
    if eoro_check == 0:
        pass
    else:
        if number-1 == -1:
            pass
        else:
            nums_list.append(number-1)
print(nums_list)

#==============================

nums_list=[n for n in range(1000) if n%2]
# range(1000) IF that item is not evenly divisible by 2. This works because if n is even, then n%2 is 0 (evenly divisible by 2) and therefore False. If n is odd, n%2 is 1, and therefore true.

#==============================

range(1,1000,2)

# ==============================

import sys
print(sys.getsizeof(range(1000)))      # 8064
print(sys.getsizeof(xrange(1000)))     # 20
print(sys.getsizeof(range(1000000)))   # 4000032 that is 4MB of RAM instead of 20 bytes
print(sys.getsizeof(xrange(1000000)))  # 20