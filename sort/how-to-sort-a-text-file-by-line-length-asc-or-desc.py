# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2501/how-to-sort-a-text-file-by-line-length-asc-or-desc_

aaa
bb
cccc
d
eeeeee
fffff

###==============================

d
bb
aaa
cccc
fffff
eeeeee

###==============================

my_list = '''aaa
bb
cccc
d
eeeeee
fffff'''.splitlines()

#with open('Gradus.txt') as in_file:
#   my_list = in_file.readlines()

print('\n'.join(sorted(my_list)))
print('=' * 5)
print('\n'.join(sorted(my_list, key=len)))
print('=' * 5)
print('\n'.join(reversed(sorted(my_list, key=len))))
print('=' * 5)

###==============================

#coding: utf-8

import sys

my_list = input

#print('\n'.join(sorted(my_list)))
#print('=' * 5)

print('\n'.join(sorted(my_list, key=len)))   #Line 10
print('=' * 5)

#print('\n'.join(reversed(sorted(my_list, key=len))))
#print('=' * 5)

###==============================

Line 10: TypeError: 'builtin_function_or_method' object is not iterable

###==============================

#coding: utf-8
import workflow

action_in = workflow.get_input()
my_list = action_in.splitlines()

print('\n'.join(my_list))
print('=' * 5)
print('\n'.join(sorted(my_list)))
print('=' * 5)
print('\n'.join(sorted(my_list, key=len)))
print('=' * 5)
print('\n'.join(reversed(sorted(my_list, key=len))))
print('=' * 5)

#: Generate the output...
action_out = '\n'.join(reversed(sorted(my_list, key=len)))
workflow.set_output(action_out)

###==============================

#coding: utf-8
import workflow
workflow.set_output('\n'.join(reversed(sorted(
    workflow.get_input().splitlines(), key=len))))

