# https://gist.github.com/jsbain/f3fc3e2d77debf98e519c6db0265bb4f

import sys,re, mmap

with open(sys.executable,'rb') as f:
	m=mmap.mmap(f.fileno(),0, access=mmap.ACCESS_READ)
	symbols=re.findall(b'@_(\w*)',m)

with open(sys.executable,'rb') as f:
	m=mmap.mmap(f.fileno(),0, access=mmap.ACCESS_READ)
	frameworks=re.findall(b'(/Sys[\w/\.]*\.framework)',m)
	
from objc_util import *

class VerboseStructure(Structure):
	def __repr__(self):
		return str(type(self))+''.join(['\n   {}:{}'.format(x[0],getattr(self,x[0])) for x in self._fields_])

from ctypes import *
class mach_header(VerboseStructure):
	_fields_ = [
	("magic", c_uint),
	("cputype", c_uint),
	("cpusubtype", c_uint),
	("filetype", c_uint),
	("ncmds", c_uint),
	("sizeofcmds", c_uint),
	("flags", c_uint)
	]					

class dyld_image_info(VerboseStructure):
	_fields_=(('imageLoadAddress',POINTER(mach_header)),
		('imageFilePath',c_char_p),
		('imageFileModDate',POINTER(c_uint)))


class dyld_all_image_infos(VerboseStructure):
	_fields_=(	('version',c_uint32),
					('infoArrayCount',c_uint32),
					('infoArray',POINTER(dyld_image_info)),
					('notification',c_void_p),
					('processEetachedFromShare',c_bool))
class load_cmd(VerboseStructure):
	_fields_=[	('cmd',c_uint32),
						('cmdsize',c_uint32)
				]
		
class segment_command(VerboseStructure):
	_fields_=[	('cmd',c_uint32),
						('cmdsize',c_uint32),
						('segname',c_char*16),
						('vmaddr', c_uint32),
						('vmsize',c_uint32),
						('fileoff',c_uint32)
				]

class symtbl_command(VerboseStructure):
	_fields_=[	('cmd',c_uint32),
						('cmdsize',c_uint32),
						('symoffset',c_uint32),
						('nsyms', c_uint32),
						('stroffset',c_uint32),
						('strsize',c_uint32)
				]
class nlist(VerboseStructure):
	_fields_=[
		('strx',c_uint32),
		('type',c_uint8),
		('sect',c_uint8),
		('desc',c_uint16),
		('value',c_uint32)
		]
c._dyld_get_all_image_infos.restype=POINTER(dyld_all_image_infos)
dyld_all_image_infos = c._dyld_get_all_image_infos()

for infoidx in range(dyld_all_image_infos[0].infoArrayCount):
	image=dyld_all_image_infos[0].infoArray[infoidx]
	print(infoidx, image.imageFilePath)
	
image=dyld_all_image_infos[0].infoArray[214]
mh=(image.imageLoadAddress[0])

pmh=addressof(mh)
cmd=load_cmd.from_address(pmh+sizeof(mh))
for idx in range( mh.ncmds):
	#do something
	if cmd.cmd==1:
		segcmd=segment_command.from_address(addressof(cmd))
		if segcmd.segname==b'__TEXT':
			textseg=segcmd
		elif segcmd.segname==b'__LINKEDIT':
			linkeditseg=segcmd
		#print(segcmd.segname,segcmd.vmaddr)
	elif cmd.cmd==2:
		symtblcmd=symtbl_command.from_address(addressof(cmd))
		print('symtbl found')
	cmd=load_cmd.from_address(addressof(cmd)+cmd.cmdsize)

file_slide = (linkeditseg.vmaddr - textseg.vmaddr) - linkeditseg.fileoff
if 1:
	#syms=cast(addressof(mh)+symtblcmd.stroffset+file_slide,POINTER(c_char))
	
	#syms2 = [x[2:] for x in syms[0:symtblcmd.strsize].split(b'\x00') if not b'$' in x]
	
	index=0
	addr=(addressof(mh)+symtblcmd.symoffset+file_slide+sizeof(nlist)*index)
	nl=(nlist).from_address(addr)
	syms=[]
	while index<symtblcmd.nsyms:
		addr=(addressof(mh)+symtblcmd.symoffset+file_slide+sizeof(nlist)*index)
		nl=(nlist).from_address(addr)	
		s=cast(addressof(mh)+symtblcmd.stroffset+file_slide+nl.strx,c_char_p).value
		if s.startswith(b'_'):
			syms.append(s[1:])
		index+=1
	
