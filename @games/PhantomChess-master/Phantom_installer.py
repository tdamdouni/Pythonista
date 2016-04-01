#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""
Run this file to download PhantomChess to the current working directory and install it in site-packages.
"""

import os
import platform
import shutil
import sys
import urllib
import zipfile

print('=' * 31)
module_name = 'Phantom'
print('Preparing to install {}...'.format(module_name))
master_name = module_name + 'Chess-master'
zip_filename = module_name + '.zip'
url = 'https://github.com/671620616/PhantomChess/archive/master.zip'

print('Downloading {}...'.format(zip_filename))
urllib.urlretrieve(url, zip_filename)
print('Unzipping {}...'.format(zip_filename))
with zipfile.ZipFile(zip_filename, 'r') as zipped:
    zipped.extractall()
print('Adding {} to importable location...'.format(module_name))
for p in sys.path:
    if os.path.split(p)[1] == 'site-packages':
        copy_to = os.path.join(p, module_name)
        try:
            shutil.rmtree(copy_to)
        except OSError:
            pass
        try:
            shutil.copytree(os.path.join(master_name, module_name), copy_to)
            print('Successfully copied {} to: {}'.format(module_name, copy_to))
        # a homebrew installed Python on Mac OS X has a read-only /Library/Python/2.7/site-packages
        except OSError as e:
            fmt = 'Warning: Failed to copy {} to: {} ({})'
            print(fmt.format(module_name, copy_to, e))

print('Cleaning up...')
try:
    shutil.rmtree(module_name)
except OSError:
    pass
shutil.copytree(os.path.join(master_name, module_name), module_name)
shutil.rmtree(master_name)
os.remove(zip_filename)


def unix_chmod_plus_x(file_path='Phantom/Run_this.py'):
    platform_sys = platform.system()
    if ((platform_sys == 'Darwin' and platform.machine().startswith('iP'))  # on iOS
      or platform_sys in ('Windows', 'Java')):  # not on unix
        return
    try:
        import stat

        plus_x = os.stat(file_path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(file_path, plus_x)
        fmt = 'To run {} from the command line, type: {}'
        print(fmt.format(module_name, file_path))
    except ImportError:
        pass


unix_chmod_plus_x(module_name + '/Run_this.py')
print('Done! {}'.format('=' * 25))
