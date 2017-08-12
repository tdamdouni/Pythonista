# https://forum.omz-software.com/topic/4278/is-it-possible-to-update-a-file-without-modifying-its-ctime/5

from objc_util import ObjCClass
import editor

NSFileManager = ObjCClass('NSFileManager')
NSFileCreationDate = 'NSFileCreationDate'

attrs = NSFileManager.defaultManager().attributesOfItemAtPath_error_(ns(editor.get_path()), None)
creation_date = attrs[NSFileCreationDate]

print('File name: {}'.format(editor.get_path()))
print('File creation date: {}'.format(creation_date))
print('File creation timestamp: {}'.format(creation_date.timeIntervalSince1970()))

# Console output

# File name: /private/var/mobile/Containers/Shared/AppGroup/6644AB67-CC6B-4108-B96C-5DCDAC15FB7C/Pythonista3/Documents/birthtime.py
# File creation date: 2017-08-11 14:55:52 +0000
# File creation timestamp: 1502463352.8284547