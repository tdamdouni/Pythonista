# coding: utf-8

# https://forum.omz-software.com/topic/2382/git-or-gist-workflow-for-pythonista/22

from __future__ import print_function
import os
import shutil


_git_dir = '.git'
_url = 'https://github.com/Phuket2/Pythonista'
_cmd_git_clone = 'git clone {} > &3'
_cmd_cd = 'cd {}'

from stash import stash

_stash = stash.StaSh()
_stash(_cmd_cd.format(os.curdir))

if os.path.exists(_git_dir):
	print('we have a git dir already')
	shutil.rmtree(_git_dir)
	
	
cmd = _cmd_git_clone.format(_url)
print(cmd)
print(_stash(cmd))


#==============================

# coding: utf-8
import os
import shutil
import editor

'''
    ONLY TESTING...DESTRUCTIVE
'''

this_path , fn = os.path.split(editor.get_path())

_git_dir = '.git'
_url = 'https://github.com/Phuket2/Pythonista.git'
_cmd_git_clone = 'git clone {} > &3'
_cmd_cd = 'cd {} > &3'
_clone_dir_name = 'git_clone'
_cmd_mkdir = 'mkdir {}'


from stash import stash

_stash = stash.StaSh()
_stash(_cmd_cd.format(this_path))
_stash(_cmd_mkdir.format(_clone_dir_name))
_stash(_cmd_cd.format(_clone_dir_name))

if os.path.exists(_git_dir):
	print('we have a git dir already')
	shutil.rmtree(_git_dir)
	
	
cmd = _cmd_git_clone.format(_url)
print(_stash(cmd))

