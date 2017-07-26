# https://gist.github.com/omz/aca3f4877d3f565239d8

# https://forum.omz-software.com/topic/3996/easily-toggling-display-s-white-point-accessibility/2

# https://twitter.com/olemoritz/status/713104304366886916

from ctypes import *
from objc_util import *
import json
import os
import ui

mach_task_self = c.mach_task_self
mach_task_self.restype = c_void_p
IOServiceGetMatchingService = c.IOServiceGetMatchingService
IOServiceGetMatchingService.argtypes = [c_uint, c_void_p]
IOServiceGetMatchingService.restype = c_void_p
IOServiceMatching = c.IOServiceMatching
IOServiceMatching.argtypes = [c_char_p]
IOServiceMatching.restype = c_void_p
IOMobileFramebufferOpen = c.IOMobileFramebufferOpen
IOMobileFramebufferOpen.argtypes = [c_uint, c_uint, c_void_p, c_void_p]
IOMobileFramebufferOpen.restype = c_int
IOMobileFramebufferGetGammaTable = c.IOMobileFramebufferGetGammaTable
IOMobileFramebufferGetGammaTable.argtypes = [c_void_p, c_void_p]
IOMobileFramebufferGetGammaTable.restype = c_int
IOMobileFramebufferSetGammaTable = c.IOMobileFramebufferSetGammaTable
IOMobileFramebufferSetGammaTable.argtypes = [c_void_p, c_void_p]
IOMobileFramebufferSetGammaTable.restype = c_int

def set_gamma(red=1.0, green=1.0, blue=1.0):
	rs = int(red * 0x100)
	gs = int(green * 0x100)
	bs = int(blue * 0x100)
	self_port = mach_task_self()
	s = IOServiceMatching(b'AppleCLCD')
	service = IOServiceGetMatchingService(0, s)
	fb = c_void_p()
	error = IOMobileFramebufferOpen(service, self_port, 0, byref(fb))
	GammaTable = c_uint32 * 771
	data = GammaTable()
	for i in range(771):
		data[i] = 0
	if os.path.exists('gammatable.json'):
		with open('gammatable.json', encoding='utf-8') as f:
			table = json.load(f)
			for i, value in enumerate(table):
				data[i] = value
	else:
		IOMobileFramebufferGetGammaTable(fb, byref(data))
		values = [data[i] for i in range(771)]
		with open('gammatable.json', 'w') as f:
			json.dump(values, f)
	for i in range(256):
		j = 255 - i
		r = j * rs >> 8
		g = j * gs >> 8
		b = j * bs >> 8
		data[j + 0x001] = data[r + 0x001]
		data[j + 0x102] = data[g + 0x102]
		data[j + 0x203] = data[b + 0x203]
	IOMobileFramebufferSetGammaTable(fb, data)

def apply_gamma(sender):
	v = sender.superview
	r = v['r_slider'].value
	g = v['g_slider'].value
	b = v['b_slider'].value
	set_gamma(r, g, b)

data = '''\
QlpoOTFBWSZTWQTh4qsAAlxfgFUQUGd/8D+AGYq/r9/qQAIcHXEAwAAAAGgAAAAAaRMaIZ
MpoIwAEbQQYACMqTQDIxNA0wAJkAGhkwRSaRGmQKeFPUGTQ0aDxQPKZNlLEcFSFB+DeHTr
fITBWKsAy3tjIywrZYWgANogHqECyGEcQg0QrAStJ5vTe8JHxWrzaoyFiQGK/ps4wS5Hey
1atXu1d1wJuYdu5puKNWslGkMtayy1rFGawBVfiMjw2aoiAyktGWAe1hDAPdA5XEuMAwER
40i40qqNTlTEgyEkgkoQSSiIKY1xOFUSX3kEMQUVKsAPh4KlwfS/Nm3BWcg3wkYWAONCTg
C2IKS7j1SdDZalAEuCittIxGmtyloYCTOgje55VRvMdRVE6CZS24bEnBSDrnmk1tcWAgCn
BScpLlIsBUKfge9CUrayl6p6potmks9oJ5ACQGHJkKzN3A+/T+q8vIOFcrzDq1DEvZjbX/
LA748gpRfEeAS1aJdRC7zDMp1eUQ3hqCKBhqFqF1gbgsBzPTAMjah53L0A0Bt2hneg+gda
9XWFFZcekM0BqDYGUaOgc2nBvcjeMLkzrOgNsaVtAvDEGtuXOGcNAWBRuDZaGNz4nLoC4c
EtcZyYfyELDYs9j22c1qd7x7+NJ+4/8XckU4UJAE4eKrA=
'''
import ui
import bz2
from base64 import b64decode
pyui = bz2.decompress(b64decode(data))
v = ui.load_view_str(pyui.decode('utf-8'))
v.present('sheet')
