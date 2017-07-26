# https://forum.omz-software.com/topic/3946/how-to-improve-speed-of-drawing-very-slow-scene-view/4

from scene import *
import ui

glyphsDict = {}  # My dictionary with paths to draw

class MyScene (Scene):
	def setup(self):
	
		self.myPath = ShapeNode(glyphsDict[1])  # first path to draw
		self.add_child(self.myPath)
		
		self.background_color = 'lightgrey'
		
	def touch_began(self, touch):
		x, y = touch.location
		z = int(x/(10.24/2)+1)
		self.myPath.path = glyphsDict[z]  # Setting a new path to draw
		
	def touch_moved(self, touch):
		x, y = touch.location
		z = int(x/(10.24/2)+1)
		self.myPath.path = glyphsDict[z]  # Setting a new path to draw
		
run(MyScene())

# --------------------

from scene import *
import ui

glyphsDict = {i:ui.Path.oval(0,0,10+i, 10+i) for i in range(200)}

class MyScene (Scene):
	def setup(self):
		self.center = self.size/2
		self.myPath = ShapeNode(glyphsDict[0], fill_color='red',
		position=self.center,
		parent=self)
		self.background_color = 'grey'
		
	def touch_began(self, touch):
		x, y = touch.location
		x = x - self.center.x
		z = int(abs(x/5.0))%len(glyphsDict)
		self.myPath.path = glyphsDict[z]  # Setting a new path to draw
		
	def touch_moved(self, touch):
		x, y = touch.location
		x = x - self.center.x
		z = int(abs(x/5.0))%len(glyphsDict)
		self.myPath.path = glyphsDict[z]  # Setting a new path to draw
		
run(MyScene(), show_fps=True)

# --------------------

from scene import *
import ui


from objc_util import *
glyphsDict = {}
for i in range(96):
	font=ObjCClass('UIFont').systemFontOfSize_weight_(32+i,1)
	s='a' #'Hello world'
	p=ui.Path()
	p.line_width = 1
	w=0
	
	c.CTFontCreatePathForGlyph.restype = c_void_p
	c.CTFontCreatePathForGlyph.argtypes = [c_void_p, c_void_p, c_void_p]
	
	x = s.encode('ascii')[0]
	glyph=  font._defaultGlyphForChar_(x)
	if not x==32: #space
		letter = ObjCInstance(c.CTFontCreatePathForGlyph(font, glyph, None))
		letterBezier=UIBezierPath.bezierPathWithCGPath_(letter)
		#transform it so we shift and flip y
		letterBezier.applyTransform_(CGAffineTransform(1,0,0,-1,w,font.capHeight()))
		ObjCInstance(p).appendBezierPath_(letterBezier)
	w+=font.advancementForGlyph(glyph).width
	glyphsDict[i] = p
	
#glyphsDict = {i:ui.Path.oval(0,0,10+i, 10+i) for i in range(200)}

class MyScene (Scene):
	def setup(self):
		self.center = self.size/2
		self.myPath = ShapeNode(glyphsDict[0], stroke_color='red',
		position=self.center,
		parent=self)
		self.background_color = 'grey'
		
	def touch_began(self, touch):
		x, y = touch.location
		x = x - self.center.x
		z = int(abs(x/5.0))%len(glyphsDict)
		self.myPath.path = glyphsDict[z]  # Setting a new path to draw
		
	def touch_moved(self, touch):
		x, y = touch.location
		x = x - self.center.x
		z = int(abs(x/5.0))%len(glyphsDict)
		self.myPath.path = glyphsDict[z]  # Setting a new path to draw
		
run(MyScene(), show_fps=True)

# --------------------

