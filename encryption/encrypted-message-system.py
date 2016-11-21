# coding: utf-8

# https://forum.omz-software.com/topic/2943/trying-to-make-an-encrypted-message-system/5

import string

char_list = list(string.ascii_letters) + list(string.digits) + list(string.punctuation)


def encrypt(message, key):
	alphabet = string.ascii_letters
	shifted_alphabet = alphabet[key:] + alphabet[:key]
	table = string.maketrans(alphabet, shifted_alphabet)
	return message.translate(table)
	
	
def decrypt(message, key):
	alphabet = string.ascii_letters
	shifted_alphabet = alphabet[-key:] + alphabet[:-key]
	table = string.maketrans(alphabet, shifted_alphabet)
	return message.translate(table)

