# coding: utf-8

# https://forum.omz-software.com/topic/2886/stash-ui-for-git-cmds

import os
import shutil
import editor

'''
    ONLY TESTING  
'''

this_path , fn = os.path.split(editor.get_path())

_git_dir = '.git'
_cmd_git_clone = 'git clone {} > &3'
_cmd_cd = 'cd {} > &3'
_clone_dir_name = 'git_clone'
_cmd_mkdir = 'mkdir {}'
_cmd_git_add_file = 'git add  -m {} > &3'
_cmd_git_commit = 'git commit message = hello > &3'
_cmd_git_push = 'git push origin {branch} {remote_url} -u {username} > &3'

_home_dir = os.path.join(os.path.expanduser('~') , 'Documents')
_local_dir = os.path.join(_home_dir, 'uc')
_remote = 'https://github.com/Phuket2/uc.git'

exit('Not meant to be run...Only illustration...')

from stash import stash

_stash = stash.StaSh()
# move to the dir
_stash(_cmd_cd.format(_local_dir))
# add a file/s to local index
_stash(_cmd_git_add_file.format('Test.py'))
# commit 
_stash(_cmd_git_commit.format())
# push the commits to the remote
_stash(_cmd_git_push.format(branch = 'master', remote_url = _remote,  username = 'xxx'))
