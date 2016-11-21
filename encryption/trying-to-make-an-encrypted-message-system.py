# coding: utf-8

# https://forum.omz-software.com/topic/2943/trying-to-make-an-encrypted-message-system/3

def caesar(plaintext, shift):
	alphabet = string.ascii_lowercase
	shifted_alphabet = alphabet[shift:] + alphabet[:shift]
	table = string.maketrans(alphabet, shifted_alphabet)
	return plaintext.translate(table)
# --------------------
# print "Gur rntyr syvrf ng zvqavtug".encode("rot13")
# 'The eagle flies at midnight'
# --------------------

