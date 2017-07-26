# https://forum.omz-software.com/topic/3722/listing-all-methods-in-an-objcclass/9

import sys
f=open('sys.executable','rb')
while True:
	s=f.read(10000).decode('latin1').replace('\x00','')
	if s.find('objc_msgSend') >0:
		print(f.tell())
		break
		
import sys,re, mmap

with open(sys.executable,'rb') as f:
	m=mmap.mmap(f.fileno(),0, access=mmap.ACCESS_READ)
	symbols=re.findall(b'@_(\w*)',m)

