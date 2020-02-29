from __future__ import print_function
# https://forum.omz-software.com/topic/2296/dynamic-libraries-could-it-potentially-work

# https://gist.github.com/Cethric/af84bf4130d2db8abbe3

# coding: utf-8

# ctypes method to show dynamic libraries as they are loaded. Made for Pythonista beta 1.6

import os
import ctypes
from objc_util import *

MH_MAGIC = 0xFEEDFACE
MH_CIGAM = 0xCEFAEDFE
MH_MAGIC_64 = 0xFEEDFACF
MH_CIGAM_64 = 0xCFFAEDFE
FAT_MAGIC = 0xCAFEBABE
FAT_CIGAM = 0xBEBAFECA

LC_UUID = 0x0000001B

NSUUID = ObjCClass('NSUUID')

class mach_header(ctypes.Structure):
    _fields_ = [
                ('magic', ctypes.c_uint32),
                ('cputype', ctypes.c_uint32),
                ('cpusubtype', ctypes.c_uint32),
                ('filetype', ctypes.c_uint32),
                ('ncmds', ctypes.c_uint32),
                ('sizeofcmds', ctypes.c_uint32),
                ('flags', ctypes.c_uint32),
                ]


class mach_header_64(ctypes.Structure):
    _fields_ = [
                ('magic', ctypes.c_uint32),
                ('cputype', ctypes.c_uint32),
                ('cpusubtype', ctypes.c_uint32),
                ('filetype', ctypes.c_uint32),
                ('ncmds', ctypes.c_uint32),
                ('sizeofcmds', ctypes.c_uint32),
                ('flags', ctypes.c_uint32),
                ('reserved', ctypes.c_uint32),
                ]
                

class dl_info(ctypes.Structure):
    _fields_ = [
                ('dli_fname', ctypes.POINTER(ctypes.c_char_p)),
                ('dli_fbase', ctypes.POINTER(ctypes.c_void_p)),
                ('dli_sname', ctypes.POINTER(ctypes.c_char_p)),
                ('dli_saddr', ctypes.POINTER(ctypes.c_void_p)),
                ]
                

class load_command(ctypes.Structure):
    _fields_ = [
                ('cmd', ctypes.c_uint32),
                ('cmdsize', ctypes.c_uint32),
                ]
                

class uuid_command(ctypes.Structure):
    _fields_ = [
                ('cmd', ctypes.c_uint32),
                ('cmdsize', ctypes.c_uint32),
                ('uuid', ctypes.c_uint8 * 16),
                ]
                

class segment_command(ctypes.Structure):
    _fields_ = [
                ('cmd', ctypes.c_uint32),
                ('cmdsize', ctypes.c_uint32),
                ('segname', ctypes.c_char * 16),
                ('vmaddr', ctypes.c_uint32),
                ('vmsize', ctypes.c_uint32),
                ('fileoff', ctypes.c_uint32),
                ('filesize', ctypes.c_uint32),
                ('maxprot', ctypes.c_uint32),
                ('initprot', ctypes.c_uint32),
                ('nsects', ctypes.c_uint32),
                ('flags', ctypes.c_uint32),
                ]


def _image_header_size(mh):
    is_header_64_bit = mh.magic == MH_MAGIC_64 or mh.magic == MH_CIGAM_64
    return ctypes.sizeof(mach_header_64) if is_header_64_bit else ctypes.sizeof(mach_header)

def _image_retrieve_uuid(mh):
    size = _image_header_size(mh)
    cursor = ctypes.addressof(mh) + size
    segmentCommand = segment_command()
    for i in range(0, int(mh.ncmds)):
        cursor += int(segmentCommand.cmdsize)
        segmentCommand = ctypes.cast(cursor, ctypes.POINTER(segment_command)).contents
        if segmentCommand.cmd == LC_UUID:
            uuidCommand = ctypes.cast(cursor, ctypes.POINTER(uuid_command)).contents
            return NSUUID.alloc().initWithUUIDBytes_(uuidCommand.uuid).UUIDString()
        

def print_image(mh, added):
    image_info = dl_info()
    func = c.dladdr
    func.argtypes = [mach_header, ctypes.POINTER(dl_info)]
    func.restype = ctypes.c_int
    result = func(mh, ctypes.byref(image_info))
    if result == 0:
        print('Could not print info for mach_header:')
        print(mh)
        return
    image_name = ctypes.string_at(image_info.dli_fname)
    image_base_address = image_info.dli_fbase.contents.value
    image_text_size = _image_header_size(mh)
    uuidt = _image_retrieve_uuid(mh)
    image_uuid = ''
    if uuidt:
        image_uuid = uuidt
    print("%s: 0x%x %s <%s>" % ('Added' if added else 'Removed', image_base_address, image_name, image_uuid))

@ctypes.CFUNCTYPE(None, ctypes.POINTER(mach_header), ctypes.c_void_p)
def dyld_add(mh, vmaddr_slide):
    print_image(mh.contents, True)

@ctypes.CFUNCTYPE(None, ctypes.POINTER(mach_header), ctypes.c_void_p)    
def dyld_removed(mh, vmaddr_slide):
    print_image(mh.contents, False)

def register_dyld_add(callback):
    func = c._dyld_register_func_for_add_image
    func.argtypes = [ctypes.c_void_p]
    func.restype = None
    return func(callback)
    
def register_dyld_removed(callback):
    func = c._dyld_register_func_for_remove_image
    func.argtypes = [ctypes.c_void_p]
    func.restype = None
    return func(callback)
    
register_dyld_add(dyld_add)
register_dyld_removed(dyld_removed)