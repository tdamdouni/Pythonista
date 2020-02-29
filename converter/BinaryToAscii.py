from __future__ import print_function
# https://gist.github.com/lglfa/8bf6c6a0188d6dada3a36d1837f5ed60

import binascii
a = binascii.a2b_hex('11')
a_samw= '\x11'
b= binascii.b2a_hex(a)
b_same = binascii.b2a_hex(a_samw)
print(b,b_same)

