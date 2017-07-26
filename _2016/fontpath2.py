# https://gist.github.com/jsbain/b5a56a632996041888be9df56a5d27e3

# https://forum.omz-software.com/topic/3933/get-bezier-path-from-text/2

#  I think you need to set restype and argtypes for CTFontCreatePathForGlyph. It may happen to work for you because you are using (I think) a 32-bit device.

from objc_util import *
import ui
font=ObjCClass('UIFont').systemFontOfSize_weight_(64,1)
s='Hello world'
p=ui.Path()
w=0

for x in s:
	glyph=	font.glyphWithName_(x)
	if glyph:
		letter = ObjCInstance(c.CTFontCreatePathForGlyph(font, glyph, None))
		letterBezier=UIBezierPath.bezierPathWithCGPath_(letter)
		#transform it so we shift and flip y
		letterBezier.applyTransform_(CGAffineTransform(1,0,0,-1,w,font.capHeight()))
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


