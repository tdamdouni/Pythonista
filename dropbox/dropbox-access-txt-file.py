# coding: utf-8

# https://forum.omz-software.com/topic/1521/dropbox-access-txt-file/5

from __future__ import print_function
import contextlib, dropboxlogin
filename = '2048.py'
dropbox_client = dropboxlogin.get_client()
with contextlib.closing(dropbox_client.get_file(filename)) as in_file:
    data = in_file.read()
print(data)

# --------------------

# Here is a 6 liner that simply uploads, then downloads a textfile, which makes use of the generated token to make things easy. You can replace the test string with an open file object

import dropbox,contextlib
TOKEN='YOUR ACCESS TOKEN GOES HERE... GENERATE FROM DROPBOX API PAGE'
d=dropbox.Dropbox(TOKEN)
d.files_upload('test','/test.txt')
with contextlib.closing(d.files_download('/test.txt')[1]) as response:
    print(response.content)

# --------------------
