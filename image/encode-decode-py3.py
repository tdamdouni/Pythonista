# coding: utf-8

# https://forum.omz-software.com/topic/2974/need-python-script-to-decode-or-encode-in-base64/6

from __future__ import absolute_import
from __future__ import print_function
import base64
import clipboard
decoded = clipboard.get()
decoded = decoded.encode('ascii')
encoded =base64.b64encode (decoded)
clipboard.set(encoded)
print("Encoded Value:" ,encoded, end=' ')

# you did not say what error you get, but i can guess it relates to unicode vs bytes.

# base64.encode takes a bytes object, you are giving it a string.
# try replaceing decoded with decoded.encode('ascii') before passing into base64.b64encode

