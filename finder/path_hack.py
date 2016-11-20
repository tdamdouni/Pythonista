# coding: utf-8

# https://forum.omz-software.com/topic/2017/html-web-export/5

import os

print('=' * 40)
print(os.curdir)
print(os.getcwd())
print(os.path.abspath(os.getcwd()))
print(os.path.realpath(os.getcwd()))
print(os.path.relpath(os.getcwd(), os.path.expanduser('~')))
print('=' * 20)
home_dir = os.path.expanduser('~')
print('home_dir', home_dir)
assert os.path.expanduser(os.environ['HOME']) == home_dir, 'Always True?'
assert os.path.expanduser(os.environ.get('HOME')) == home_dir, 'Always True?'
docs_dir = os.path.expanduser('~/Documents')
print('docs_dir', docs_dir)
script_dir, script_name = os.path.split(__file__)
print('script_dir', script_dir, 'script_name', script_name)
app_path = os.path.abspath(os.path.join(os.__file__, '../..'))
print('app_path', app_path)
print('=' * 20)
print('\n'.join(file_or_folder_name for file_or_folder_name in os.listdir(os.curdir)))
print('=' * 20)
print('\n'.join(file_or_folder_name for file_or_folder_name in os.listdir(home_dir)))
print('=' * 20)
print('\n'.join(folder_name for folder_name in os.listdir(home_dir)
                if os.path.isdir(os.path.join(home_dir, folder_name))))
print('=' * 20)
print('\n'.join(file_name for file_name in os.listdir(home_dir)
                if os.path.isfile(os.path.join(home_dir, file_name))))

# also see: files_and_folders.py and cd_ls_pwd

