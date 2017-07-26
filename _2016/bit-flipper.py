# coding: utf-8

# https://github.com/cclauss/Ten-lines-or-less/blob/master/bit_filpper.py

# https://forum.omz-software.com/topic/2943/trying-to-make-an-encrypted-message-system
# a poor man's encryption


def bit_flipper(s, salt=1):
    return ''.join([chr(ord(x) ^ salt) for x in s])

salt = 1  # try 1, 6, 7
# for instance, salt = 2 gives you an encrypted string with no printable chars
# (disappearing ink)!
s = 'Pythonista rules!   ¥€$ īt döèš'
print(s)
s = bit_flipper(s, salt)
print(s)
s = bit_flipper(s, salt)
print(s)
