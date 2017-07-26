# https://gist.github.com/jsbain/9e9b039512912b7d4f0c35a28ef708a1

import sys,re, mmap

'''static libs/syms
with open(sys.executable,'rb') as f:
	m=mmap.mmap(f.fileno(),0, access=mmap.ACCESS_READ)
	symbols=re.findall(b'@_(\w*)',m)

with open(sys.executable,'rb') as f:
	m=mmap.mmap(f.fileno(),0, access=mmap.ACCESS_READ)
	frameworks=re.findall(b'(/Sys[\w/\.]*\.framework)',m)
'''
from objc_util import *

class VerboseStructure(Structure):
	def __repr__(self):
		return str(type(self))+''.join(['\n   {}:{}'.format(x[0],getattr(self,x[0])) for x in self._fields_])

from ctypes import *
class mach_header(VerboseStructure):
	_fields_ = [
	("magic", c_uint32),
	("cputype", c_uint32),
	("cpusubtype", c_uint32),
	("filetype", c_uint32),
	("ncmds", c_uint32),
	("sizeofcmds", c_uint32),
	("flags", c_uint32)
	]					

class dyld_image_info(VerboseStructure):
	_fields_=(('imageLoadAddress',POINTER(mach_header)),
		('imageFilePath',c_char_p),
		('imageFileModDate',POINTER(c_uint)))

#dont need the whole structure...
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
						('fileoff',c_uint)
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

def print_libs():
	for infoidx in range(dyld_all_image_infos[0].infoArrayCount):
		image=dyld_all_image_infos[0].infoArray[infoidx]
		print(infoidx, image.imageFilePath)

def syms_for_idx(idx):
	image=dyld_all_image_infos[0].infoArray[idx]
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
			#print('symtbl found')
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
		return syms

import ui
class LoadedLibrariesDataSource(object):

	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return dyld_all_image_infos[0].infoArrayCount

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		image=dyld_all_image_infos[0].infoArray[row]
		cell.text_label.text = image.imageFilePath.split(b'/')[-1].decode()
		return cell

	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return False

	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return False
	def tableview_did_select(self,tableview,section,row):
		back=ui.ButtonItem()
		back.title='Back'
		_src=tableview.data_source
		def a(sender):
			tableview.data_source=_src
			tableview.delegate=_src
			tableview.left_button_items=[]
			tableview.reload()
			tableview.name=''
		back.action=a
		tableview.data_source=tableview.delegate=SymbolsDataSource(row)
		tableview.reload()
		tableview.left_button_items=[back]
		image=dyld_all_image_infos[0].infoArray[row]
		tableview.name=image.imageFilePath.split(b'/')[-1].decode()
class SymbolsDataSource(object):
	def __init__(self,infoidx):
		
		self.syms=syms_for_idx(infoidx)
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.syms)

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()

		cell.text_label.text = self.syms[row].decode()
		return cell

	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return False

	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return False
t=ui.TableView()
t.frame=(0,0,400,700)
t.data_source=LoadedLibrariesDataSource()
t.delegate=t.data_source
t.present()

