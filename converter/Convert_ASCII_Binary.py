# -*- coding: utf-8 -*-

# https://gist.github.com/eduardoedson/d3e659cf02761c0074f56db5de337a7b
import binascii
import os


def to_binary(frase):
	return bin(int(binascii.hexlify(frase), 16))
	
def to_ascii(frase):
	return binascii.unhexlify('%x' % int(frase, 2))
	
# ======================================================================
function = raw_input('[1] - Passar para ASCII\n[2] - Passar para Binário\n')
frase = raw_input('\nQual a frase?\n')
os.system('clear')

if int(function) == 1:
	print('Frase em Binário: ' + frase)
	print('Frase em ASCII: ' + to_ascii(frase))
elif int(function) == 2:
	print('Frase em ASCII: ' + frase)
	print('Frase em Binário: ' + to_binary(frase))
else:
	print('Opção inválida')

