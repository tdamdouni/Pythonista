from __future__ import print_function
#The basic outline of this problem is to read the file, look for integers using the refindall
#looking for a regular expression of [0-9]+ and then converting the extracted strings 
#to integer and summing up the integers.

import re

hand = open('regex_sum_297209.txt')
numlist = list()

for line in hand:
    line = line.rstrip()
    x = re.findall('([0-9]+)', line)
    if len(x) > 0:
        for i in x:
            print(i)
            num = float(i)
            numlist.append(num)

print(sum(numlist))