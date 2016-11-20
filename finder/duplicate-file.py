#!python2

# https://forum.omz-software.com/topic/3586/duplicate-a-directory-or-multiple-files/4

import os
import shutil
cwd = os.getcwd()
src = '/private/var/mobile/Containers/Shared/AppGroup/7D138C58-C42A-47A7-80FB-2D57A2A06406/Documents/Sync/DropboxSync.py' # change for the good adress
dst = cwd+'/Sync/@duplicates/DropboxSync.py'
print(src)
print(dst)
shutil.copytree(src,dst)

