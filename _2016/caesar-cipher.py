#! Python2

# https://forum.omz-software.com/topic/2943/trying-to-make-an-encrypted-message-system/2

# http://stackoverflow.com/questions/8886947/caesar-cipher-function-in-python

import string

def caesar(plaintext, shift):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = string.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)
