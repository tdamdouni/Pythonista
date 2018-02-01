# https://gist.github.com/jsbain/1b5066eebac9467accabaec88e993f46

# https://forum.omz-software.com/topic/4377/lmza-should-technically-be-possible/4

from ctypes import *
COMPRESSION_LZMA = 0x306

c=CDLL(None)

def encode(instr):
	outbuf = create_string_buffer(max(32767,len(instr)))
	inbuf = create_string_buffer(len(instr))
	insz=len(instr)
	inbuf[:len(instr)]=instr
	outsz=c.compression_encode_buffer(addressof(outbuf), sizeof(outbuf), addressof(inbuf),insz,None,COMPRESSION_LZMA)
	return outbuf[:outsz]
def decode(instr,outsz):
	#we have to guess outsz, and keep trying i guess
	#better to use streaming methods
	outbuf = create_string_buffer(outsz)
	inbuf = create_string_buffer(len(instr))
	insz=len(instr)
	inbuf[:len(instr)]=instr
	while True:
		outwritten=c.compression_decode_buffer(addressof(outbuf), sizeof(outbuf), addressof(inbuf), insz, None, COMPRESSION_LZMA)
		if outwritten==outsz:
			outsz=4*outsz
			outbuf = create_string_buffer(outsz)
		else:
			break
	return outbuf[:outwritten]
encoded=encode(b'hello world')
decoded=decode(encoded,100)
print(decoded)
