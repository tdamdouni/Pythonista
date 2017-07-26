# https://forum.omz-software.com/topic/3933/get-bezier-path-from-text/9

from objc_util import *
import ui
font=ObjCClass('UIFont').systemFontOfSize_weight_(64,1)
s='Hello world'
p=ui.Path()
w=0

c.CTFontCreatePathForGlyph.restype = c_void_p
c.CTFontCreatePathForGlyph.argtypes = [c_void_p, c_void_p, c_void_p]

for x in s.encode('ascii'):
    glyph=  font._defaultGlyphForChar_(x)
    if not x==32: #space
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
