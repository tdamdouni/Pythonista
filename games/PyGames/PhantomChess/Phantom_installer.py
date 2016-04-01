#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run this file to download PhantomChess to the current working directory and install it in site-packages.
"""
print('=' * 31)

import os
import platform
import shutil
import sys
import urllib
import zipfile

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
        copyto = os.path.join(p, module_name)
        try:
            shutil.rmtree(copyto)
        except:
            pass
        try:
            shutil.copytree(os.path.join(master_name, module_name), copyto)
            print('Successfully copied {} to: {}'.format(module_name, copyto))
# a homebrew installed Python on Mac OS X has a read-only /Library/Python/2.7/site-packages
        except OSError as e:
            print('Failed to copy {} to: {} ({})'.format(module_name, copyto, e))
print('Cleanng up...')
try:
    shutil.rmtree(module_name)
except:
    pass
shutil.copytree(os.path.join(master_name, module_name), module_name)
shutil.rmtree(master_name)
os.remove(zip_filename)

def unix_chmod_plus_x(filepath= 'Phantom/Run_this.py'):
    platform_sys = platform.system()
    if ((platform_sys == 'Darwin' and platform.machine().startswith('iP'))  # on iOS
      or platform_sys in ('Windows', 'Java')):                              # not on unix
        return 
    try:
        import stat
        plus_x = os.stat(filepath).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(filepath, plus_x)
        fmt = 'To run {} from the command line, type: {}'
        print(fmt.format(module_name, filepath))
    except ImportError:
        pass
unix_chmod_plus_x(module_name + '/Run_this.py')
print('Done! {}'.format('=' * 25))
