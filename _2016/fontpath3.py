# https://gist.github.com/jsbain/761de9d628d2a6689d73a00d24ac2a53

from objc_util import *
import ui
import ctypes
font=ObjCClass('UIFont').systemFontOfSize_weight_(64,1)
s='Hello world'
p=ui.Path()
w=0
CGGlyph = ctypes.c_ushort
c.CTFontCreatePathForGlyph.argtypes=[c_void_p, ctypes.c_ushort, POINTER(CGAffineTransform)]
c.CTFontCreatePathForGlyph.restype=c_void_p

for x in s:
	glyph=	font.glyphWithName_(x)
	if glyph:
		#transform it so we shift and flip y
		letter = ObjCInstance(c.CTFontCreatePathForGlyph(font, 
				glyph, 
				CGAffineTransform(1,0,0,-1,w,font.capHeight())))
				
		letterBezier=UIBezierPath.bezierPathWithCGPath_(letter)
		ObjCInstance(p).appendBezierPath_(letterBezier)
	w+=font.advancementForGlyph(glyph).width

class myview(ui.View):
	def __init__(self):
		self.frame=(0,0,500,500)
		self.bg_color='white'
	def draw(self):
		ui.set_color('red')
		p.line_width=1
		p.stroke()
myview().present('sheet')


