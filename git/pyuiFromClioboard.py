# coding: utf-8

# https://forum.omz-software.com/topic/2524/codeshare-animated-view

# With this script (in the same directory) you can copy your pyui file to the clipboard and then via webinterface in a new github file.

from __future__ import print_function
import os
import sys
import clipboard

path = os.getcwd()
files = []
for item in sorted(os.listdir(path)):
  if '.pyui' in item:
    print(item, end=' ')
    files.append(item)
print()
print()
if len(files) == 1:
  filename = raw_input('Please choose pyui file or press return for [' + files[0] + ']: ') or files[0]
elif len(files) > 1:
  filename = raw_input('Please choose pyui file: ')
else:
  print('Sorry no pyui file found!')
  sys.exit()

if not '.pyui' in filename:
  filename += '.pyui'

if os.path.exists(filename):
  path += '/' + filename
  file = open(path, 'r')
  clipboard.set(file.read())
  file.close()
  print(filename + ' is in clipboard.')
else:
  print("Can't find " + filename)