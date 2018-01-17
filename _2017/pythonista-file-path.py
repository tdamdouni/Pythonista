# https://forum.omz-software.com/topic/4532/editor-module-question/2

import os
os.path.expanduser('~/Documents/Brain/yourfile.txt')

import os
_root_path = os.path.expanduser('~/Documents')
_my_dir = 'Brain'
_my_file_name = 'yourfile.txt'

my_path = os.path.join(_root_path, _my_dir, _my_file_name)

print(my_path)

with open(my_path, "w") as f:
    f.writelines("Hello World")
