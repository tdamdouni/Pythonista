# coding: utf-8

# https://forum.omz-software.com/topic/2974/need-python-script-to-decode-or-encode-in-base64

from __future__ import print_function
import base64
encsting = raw_input('Encoded Value:')
decstring = base64.b64decode(encsting)
print(decstring)

# ...

import base64
import clipboard
encsting = clipboard.get()
decstring = base64.b64decode(encsting)
clipboard.set(decstring)

