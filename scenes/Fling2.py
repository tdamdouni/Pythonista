"""
100% of this code was written and tested in the Pythonista iOS app
"""

from scene import *
from random import random
import math


def intersect(a, b):
	import math
	if (a.w==0 and b.w==0):
		return None
	try:
		if (a.h/a.w == b.h/b.w):
			return None
	except:
		pass
	if a.w==0:
		Fb = lambda x: (b.h/b.w)*x+(b.y-(b.x*b.h/b.w))
		if (min(a.y, a.y+a.h) <= Fb(a.x)<= max(a.y, a.y + a.h)) and (min(b.x, b.x+b.w) <= a.x <= max(b.x, b.x + b.w)):
			return (a.x, Fb(a.x))
		else:
			return None
	elif b.w==0:
		Fa = lambda x: (a.h/a.w)*x+(a.y-(a.x*a.h/a.w))
		if (b.y <= Fa(b.x) <= b.y + b.h) and (a.x <= b.x <= a.x + a.w):
			return (b.x, Fa(b.x))
		else:
			return None
	else:
		Sa = a.h/a.w
		Ma = a.y-a.x*a.h/a.w
		Sb = b.h/b.w
		Mb = b.y-b.x*b.h/b.w
		Fb = lambda x: (b.h/b.w)*x+(b.y-(b.x*b.h/b.w))
		Px = (Ma - Mb) / (Sb - Sa)
		if (min(a.x,a.x+a.w) <= Px <= max(a.x, a.x + a.w)) and (min(b.x, b.x+b.w) <= Px <= max(b.x, b.x + b.w)):
			return (Px, Fb(Px))
		else:
			return None
			
def perp(b, intersection):
	import math
	length = (b.w**2+b.h**2)**.5
	angle = math.atan2(b.h, b.w)
	newvel = (length*math.cos(angle+math.pi/2), length*math.sin(angle+math.pi/2))
	return vector(intersection[0], intersection[1], newvel[0], newvel[1])
	
def flip(v, axis):
	import math
	angleV = math.atan2(v[1], v[0])
	angleX = math.atan2(axis.h, axis.w)
	#if angleX>angleV:
	angleD = angleX-angleV
	angleN = angleX+angleD
	#else:
	#angleD = angleV-angleX
	#angleN = angleX-angleD
	length = (v[0]**2+v[1]**2)**.5
	#angleN =0 #bw collide
	return (math.cos(angleN)*length, math.sin(angleN)*length)

class vector(): #rectangle vector hybrid
	x = 0
	y = 0
	w = 0
	h = 0
	def __init__(self,x,y,w,h):
		self.x, self.y, self.w, self.h = x, y, w, h
		
class token():
	transform = vector(0,0,0,0)
	type = "" #"goal", "coin", "enemy"
	
class Text():
	text = ""
	font = "Helvetica"
	size = 0
	color = (0,0,0)
	def __init__(self, text="", font="Helvetica", size=0, color=(0,0,0)):
		self.text = text
		self.font = font
		self.size = size
		self.color = color
		
class guiElement():
	bg = (0,0,0)
	textpadding = (0,0)
	bgalpha = 0
	isClickable = False
	label = Text()
	transform = vector(0,0,0,0)
	def __init__(self, transform, bg=(1,1,1), label=Text(), isClickable=False):
		self.transform = transform
		self.bg = bg
		self.label = label
		self.isClickable = isClickable
	def draw(self):
		stroke(self.bg[0], self.bg[1], self.bg[2])
		fill(self.bg[0], self.bg[1], self.bg[2])
		if not self.bgalpha:
			rect(self.transform.x, self.transform.y, self.transform.w, self.transform.h)
		tint(self.label.color[0],self.label.color[1],self.label.color[2])
		textrender = render_text(self.label.text, self.label.font, self.label.size)
		self.transform = vector(self.transform.x, self.transform.y, textrender[1].w, textrender[1].h)
		image(textrender[0], self.transform.x,self.transform.y,textrender[1][0]+self.textpadding[0], textrender[1][1]+self.textpadding[1])
		
class Menu():
	interface = "menu"
	bg = (0,0,0)
	guiSpace = [] #[]guiElement
	def draw(self):
		for element in self.guiSpace:
			element.draw()		
		
class Level():
	interface = "level"
	bg = (0,0,0)
	spawn = vector(0,0,32,32)
	guiSpace = [] #[]guiElement
	collideSpace = [] #[]vector
	meshSpace = [] #[]vector
	tokenSpace = [] #[]token
	def draw(self):
		stroke(1,1,1)
		stroke_weight(3)
		for v in self.meshSpace:
			line(v.x, v.y, v.x+v.w, v.y+v.h)

menu1 = Menu()
title = guiElement(vector(0,0,100,100), label=Text("Fling", 'AvenirNext-Regular', 72, (0,0.62,1)))
title.transform.x = 0#-title.transform.w
print(title.transform.w)
title.bg = (0,0,0)
title.bgalpha = 0

menu1.guiSpace.append(title)
menu1.guiSpace.append(guiElement(vector(180,0,50,50), bg=(1,0,0)))
menu1.bg = (1,1,1)

level1 = Level()
level1.meshSpace = [vector(50,100, 150,100), vector(200,200,10,150)]

for v in level1.meshSpace:
	angle = math.atan2(v.h, v.w)
	#add scaling here, or maybe just in render?
	p = perp(v, (v.x+v.w/2, v.y+v.h/2))
	p = vector(p.x, p.y, 32*math.cos(math.atan2(p.h, p.w)), 32*math.sin(math.atan2(p.h, p.w)))
	#level1.collideSpace.append(p)
	p = perp(p, (p.x+p.w/2, p.y+p.h/2))
	#level1.collideSpace.append(vector(p.x, p.y, p.w/2, p.h/2))
	p = vector(p.x, p.y, ((v.w**2+v.h**2)**.5+32)*math.cos(math.atan2(p.h, p.w))/2, ((v.w**2+v.h**2)**.5+32)*math.sin(math.atan2(p.h, p.w))/2)
	level1.collideSpace.append(vector(p.x, p.y, -p.w, -p.h))
	level1.collideSpace.append(p)
	
	#level1.collideSpace.append(vector(p.x-p.w, p.y-p.h, 10,10 ))
	#level1.collideSpace.append(vector(p.x+p.w, p.y+p.h, 10,10 ))
	
	#add scaling here, or maybe just in render?
	
	d = perp(v, (v.x+v.w/2, v.y+v.h/2))
	d = vector(d.x, d.y, -32*math.cos(math.atan2(d.h, d.w)), -32*math.sin(math.atan2(d.h, d.w)))
	#level1.collideSpace.append(p)
	d = perp(d, (d.x+d.w/2, d.y+d.h/2))
	#level1.collideSpace.append(vector(p.x, p.y, p.w/2, p.h/2))
	d = vector(d.x, d.y, ((v.w**2+v.h**2)**.5+32)*math.cos(math.atan2(d.h, d.w))/2, ((v.w**2+v.h**2)**.5+32)*math.sin(math.atan2(d.h, d.w))/2)
	level1.collideSpace.append(vector(d.x, d.y, -d.w, -d.h))
	level1.collideSpace.append(d)	
	
	level1.collideSpace.append(vector(p.x-p.w, p.y-p.h, d.x-p.x,d.y-p.y ))
	level1.collideSpace.append(vector(p.x+p.w, p.y+p.h, d.x-p.x, d.y-p.y ))
	

level1.spawn.x = 200
level1.spawn.y = 500

class Game (Scene):
	def setup(self):
		#print (self.bounds)
		self.Interface = menu1
		self.position = self.bounds.center()
		#if Interface.interface == "game":
		#self.position = self.Interface.spawn
		self.dragvector = (0,0)
		self.velocity = (0,0)
		self.root_layer = Layer(self.bounds)
		self.drag = 0.99
		#add scaling here
		#self.layer = Layer(Rect(self.position.x - 16, self.position.y - 16, 32, 32))
		#self.layer.background = Color(1, 1, 1)
		#self.layer.image = ''
		#self.root_layer.add_layer(self.layer)
	
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		#0.5, 0.5, 0.8
		background(self.Interface.bg[0], self.Interface.bg[1], self.Interface.bg[2])
		
		#self.level.draw()
		
		#stroke_weight(3)
		#stroke(0.625,0.625,1)
		
		#scale level attributes up from my static display size to dynamic user screen size
		
		#for element in self.Interface.guiSpace:
		#	element.draw()
		
		#TODO: optimize
		#print(self.position.h)
		if self.Interface.interface == "game":
			###
			m = vector(self.position.x, self.position.y, self.velocity[0], self.velocity[1])
			for k in self.Interface.collideSpace:
				#try:
				d = intersect(k, m)
			#except:
				#print("zero vect")
				#d = None
			#print(d)
				if d: #there has been a collision
				#between k and velocity at d
					self.velocity = flip((-self.velocity[0], -self.velocity[1]), perp(k, d))
				
			self.velocity = (self.velocity[0]*self.drag, self.velocity[1]*self.drag)
		
			self.position.x += self.velocity[0]
			self.position.y += self.velocity[1]
		
			self.velocity = list(self.velocity)
			if self.position.x < 16:
				self.velocity[0] = abs(self.velocity[0])
			if self.position.y < 16:
				self.velocity[1] = abs(self.velocity[1])
			if self.position.x > self.bounds.w -16:
				self.velocity[0] = -abs(self.velocity[0])
			if self.position.y > self.bounds.h - 16:
				self.velocity[1] = -abs(self.velocity[1])
			self.velocity = tuple(self.velocity)
		
		#new_frame = Rect(self.position.x - 16, self.position.y - 16, 32, 32)
		#self.layer.animate('frame', new_frame, 0)
		
			stroke_weight(3)
			stroke(0.625,0.625,1)
			line(self.position.x,self.position.y,self.position.x+self.dragvector[0],self.position.y+self.dragvector[1])
		
			import math

			self.angle = math.atan2(self.dragvector[1], self.dragvector[0])
		
			if not self.dragvector==(0,0):
		
				line(self.position.x+self.dragvector[0], self.position.y+self.dragvector[1], self.position.x+self.dragvector[0]+20*math.cos(self.angle+7*math.pi/8),self.position.y+self.dragvector[1]+20*math.sin(self.angle+7*math.pi/8))
		
				line(self.position.x+self.dragvector[0], self.position.y+self.dragvector[1], self.position.x+self.dragvector[0]+20*math.cos(self.angle-7*math.pi/8),self.position.y+self.dragvector[1]+20*math.sin(self.angle-7*math.pi/8))
		
			stroke(1,1,1)	
			fill(1,1,1)
			ellipse(self.position.x - 16, self.position.y - 16, 32, 32)
		
		###
			
		self.Interface.draw()
		
		self.root_layer.update(self.dt)
		self.root_layer.draw()
		
	
	def touch_began(self, touch):
		# Animate the layer to the location of the touch:
		if self.Interface.interface == "game":
			self.startx, self.starty = touch.location.x, touch.location.y
		#new_frame = Rect(x - 16, y - 16, 32, 32)
		#self.layer.animate('frame', new_frame, 1, curve=curve_bounce_out)
		# Animate the background color to a random color:
		#new_color = Color(random(), random(), random())
		#self.layer.animate('background', new_color, 1.0)
	
	def touch_moved(self, touch):
		if self.Interface.interface == "game":
			self.dragvector = (self.startx - touch.location.x, self.starty - touch.location.y)
	
	def touch_ended(self, touch):
		if self.Interface.interface == "game":
			self.velocity = (self.velocity[0]+0.07*self.dragvector[0], self.velocity[1]+0.07*self.dragvector[1])
			self.dragvector = (0,0)
		

run(Game())
