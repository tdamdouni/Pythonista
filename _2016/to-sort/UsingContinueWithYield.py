# coding: utf-8

# https://forum.omz-software.com/topic/2735/using-continue-with-yield/4

from __future__ import print_function
def allfiles(self):
        for path, subdirs, files in os.walk(self.root_dir):
            for filename in files:
                f = os.path.join(path, filename)
                yield f

#==============================

print([filename for filename in self.allfiles() if os.path.splitext(filename)[1] == "py"])

for filename in self.allfiles():
    if os.path.dirname(filename) == os.path.expanduser("~/Documents"):
        print(filename)

#==============================

# @omz

import os
import re

def allfiles(root_dir, skip_dirs_re=None, file_ext_re=None):
    for path, subdirs, files in os.walk(root_dir):
        if skip_dirs_re:
            new_subdirs = []
            for subdir in subdirs:
                if not re.match(skip_dirs_re, subdir):
                    new_subdirs.append(subdir)
            subdirs[:] = new_subdirs
        for filename in files:
            ext = os.path.splitext(filename)[1][1:]
            if (file_ext_re is None) or (re.match(file_ext_re, ext, re.IGNORECASE)):
                full_path = os.path.join(path, filename)
                yield full_path
            
skip_dirs = '\\.Trash|site-packages'
exts = 'py|md|txt'
root_dir = os.path.expanduser('~/Documents')

for file_path in allfiles(root_dir, skip_dirs, exts):
    print(file_path)

#====================

if condition:
    print(item)


if some_skip_condition:
    continue
print(item)
