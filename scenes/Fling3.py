# https://gist.github.com/SamyBencherif/7b6a32b74fb002dc7465
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
	
def generate_colliders(meshSpace):
	collideSpace = []
	for v in meshSpace:
		angle = math.atan2(v.h, v.w)
		#add scaling here, or maybe just in render?
		p = perp(v, (v.x+v.w/2, v.y+v.h/2))
		p = vector(p.x, p.y, 32*math.cos(math.atan2(p.h, p.w)), 32*math.sin(math.atan2(p.h, p.w)))
		#level1.collideSpace.append(p)
		p = perp(p, (p.x+p.w/2, p.y+p.h/2))
		#level1.collideSpace.append(vector(p.x, p.y, p.w/2, p.h/2))
		p = vector(p.x, p.y, ((v.w**2+v.h**2)**.5+32)*math.cos(math.atan2(p.h, p.w))/2, ((v.w**2+v.h**2)**.5+32)*math.sin(math.atan2(p.h, p.w))/2)
		collideSpace.append(vector(p.x, p.y, -p.w, -p.h))
		collideSpace.append(p)
		#level1.collideSpace.append(vector(p.x-p.w, p.y-p.h, 10,10 ))
		#level1.collideSpace.append(vector(p.x+p.w, p.y+p.h, 10,10 ))
	
		#add scaling here, or maybe just in render?
	
		d = perp(v, (v.x+v.w/2, v.y+v.h/2))
		d = vector(d.x, d.y, -32*math.cos(math.atan2(d.h, d.w)), -32*math.sin(math.atan2(d.h, d.w)))
		#level1.collideSpace.append(p)
		d = perp(d, (d.x+d.w/2, d.y+d.h/2))
		#level1.collideSpace.append(vector(p.x, p.y, p.w/2, p.h/2))
		d = vector(d.x, d.y, ((v.w**2+v.h**2)**.5+32)*math.cos(math.atan2(d.h, d.w))/2, ((v.w**2+v.h**2)**.5+32)*math.sin(math.atan2(d.h, d.w))/2)
		collideSpace.append(vector(d.x, d.y, -d.w, -d.h))
		collideSpace.append(d)	
	
		collideSpace.append(vector(p.x-p.w, p.y-p.h, d.x-p.x,d.y-p.y ))
		collideSpace.append(vector(p.x+p.w, p.y+p.h, d.x-p.x, d.y-p.y ))
		
	return collideSpace


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
		
class Menu(): #minimal version of Level
	interface = "menu"
	bg = (0,0,0)
	guiSpace = [] #[]guiElement
	def touch(self, mytouch, phase):
		pass
	def draw(self):
		for element in self.guiSpace:
			pass
			#everything's in main draw right now
			#might be good because UI system is universal
			#element.draw()
			#TODO: done
		
class Level():
	interface = "level"
	bg = (0,0,0)
	spawn = vector(32,32,0,0)
	guiSpace = [] #[]guiElement
	collideSpace = [] #[]vector
	meshSpace = [] #[]vector
	tokenSpace = [] #[]token
	"""
	__update__ = None
	def update(self, t):
		self.bg, self.guiSpace, self.collideSpace, self.meshSpace, self.tokenSpace = __update__(t)
	"""
	#try as-is updating in draw
	def draw(self):
		stroke(1,1,1)
		stroke_weight(3)
		for v in self.meshSpace:
			line(v.x, v.y, v.x+v.w, v.y+v.h)
		for v in self.collideSpace:
			stroke(0.3, 0.3, 0.3)
			line(v.x, v.y, v.x+v.w, v.y+v.h)

class level1(Level):
	#level1 = Level()
	bg = (0.05, 0.7, 0.3)
	meshSpace = [vector(160,400,100,0),vector(160,400,0,100),vector(160,400,-100,0),vector(160,400,0,-100)]
	spawn = vector(160,200,0,0)
	def draw(self):
		stroke(1,1,1)
		stroke_weight(3)
		newmesh=[]
		for v in self.meshSpace:
			line(v.x, v.y, v.x+v.w, v.y+v.h)
			newangle = math.atan2(v.h, v.w)+0.005
			barlen = (v.h**2+v.w**2)**.5
			newmesh.append(vector(v.x, v.y, barlen*math.cos(newangle), barlen*math.sin(newangle)))
		self.meshSpace = newmesh
		self.collideSpace = generate_colliders(self.meshSpace)

#Interfaces

mainMenu = Menu()
#don't center text on rect x,y pos because I cannot do the same for the rectange's bounds. it get's render seperately and it's necessarily based on the classes x y values

#Rect(x=0, y=0, w=320.0, h=568.0)

mainMenu.guiSpace.append((Layer(Rect(160, 284, 0, 0)), Text("Fling", "AvenirNext-Regular", 72, (0,0.62,1))))


mainMenu.guiSpace.append((Layer(Rect(420, 316, 0, 0)), Text("Play", "AvenirNext-Regular", 72, (1,1,1))))
mainMenu.guiSpace.append((Layer(Rect(420, 242, 0, 	0)), Text("Levels", "AvenirNext-Regular", 72, (1,1,1))))

#enable this code if you want to see touch boundries
#menu1.guiSpace[0][0].background = Color(0,1,0)
#menu1.guiSpace[1][0].background = Color(0,1,0)
#menu1.guiSpace[2][0].background = Color(0,1,0)

mainMenu.bg = (1,1,1)
mainMenu.page = 0
mainMenu.name = 'menu1'


#level1.collideSpace = level1.meshSpace

#collision generator, needs to be applied to any/every level
 #4 days worth of code, turns out needs to be scrapped (*not quite*, the issue is that rectangular boundries are incorrect, points need to be equidistant from line (creating a rectangle with circles on it's ends))

level1.collideSpace = generate_colliders(level1.meshSpace)
"""
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

"""
class Game (Scene):
	#320, 568
	def setup(self):
		#print (self.bounds)
		
		self.Interface = mainMenu
		self.position = self.bounds.center()
		
		#self.Interface.guiSpace[0][0].frame.x -= self.Interface.guiSpace[0][0].frame.w/2
		#self.Interface.guiSpace[0][0].frame.y = self.Interface.guiSpace[0][0].frame.h/2
		
		#me = self.Interface.guiSpace[1][0]
		#me.animate('frame', Rect(160-me.frame.w/2,316-me.frame.h/2, self.Interface.guiSpace[1][0].frame.w, self.Interface.guiSpace[1][0].frame.h), 1)
		#me = self.Interface.guiSpace[2][0]
		#me.animate('frame', Rect(160-me.frame.w/2,242-me.frame.h/2, 0,0), 1)
		
		#this likely should be moved
		if self.Interface.interface == "game":
			self.position = self.Interface.spawn
		self.dragvector = (0,0)
		self.velocity = (0,0)
		self.root_layer = Layer(self.bounds)
		
		#self.bganim = 
		self.root_layer.animate('background', Color(1,1,1), 0)
		
		self.drag = 0.99
		
		
		for element in self.Interface.guiSpace:
				#element[0].frame.x -= element[0].frame.w/2
				#element[0].frame.y -= element[0].frame.h/2
				self.root_layer.add_layer(element[0])
		#add scaling here (or somewhere)
		
		for i in range(len(self.Interface.guiSpace)):
			element = self.Interface.guiSpace[i]
			tint(element[1].color[0], element[1].color[1], element[1].color[2])
			titleText = render_text(element[1].text, element[1].font, element[1].size)
			image(titleText[0], element[0].frame.x, element[0].frame.y, titleText[1][0], titleText[1][1])
			
			#print(self.Interface.guiSpace[i][0].frame.w-titleText[1].w)
			
			if not self.Interface.guiSpace[i][0].frame.w == titleText[1].w:
				self.Interface.guiSpace[i][0].frame.w = titleText[1].w
				self.Interface.guiSpace[i][0].frame.h = titleText[1].h
				self.Interface.guiSpace[i][0].frame.x -= self.Interface.guiSpace[i][0].frame.w/2
				self.Interface.guiSpace[i][0].frame.y -= self.Interface.guiSpace[i][0].frame.h/2
			#print(titleText[1])
				#self.setup()
			#print(titleText[1])
	
	#code that is universal to any level or menu should go here, otherwise it needs to be generalized somehow. Eg varying function reference
	def draw(self):
		
		self.root_layer.update(self.dt)
		self.root_layer.draw()
		
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		#0.5, 0.5, 0.8
		#print(self.Interface.bg)
		
		self.root_layer.animate('background', Color(self.Interface.bg[0], self.Interface.bg[1], self.Interface.bg[2]), 0.1) #cheat the time paradox
		
		#if self.bganim and self.bganim.finished:
			#print("grow")
			#background(self.Interface.bg[0], self.Interface.bg[1], self.Interface.bg[2])
		
		#self.level.draw()
		
		#stroke_weight(3)
		#stroke(0.625,0.625,1)
		
		#scale level attributes up from my static display size to dynamic user screen size
		
		if self.Interface.interface == "level":
			#print([(m.x, m.y, m.w, m.h) for m in [n for n in self.Interface.meshSpace]])
			###
			m = vector(self.position.x, self.position.y, self.velocity[0], self.velocity[1])
			for k in self.Interface.collideSpace:
				d = intersect(k, m)
				
				#for now this collision system works OK. However it needs to be majorly improved to be more accurate around the corners (test ball center distance from line < radius). The predictive nature of this collision system is good, should be maintained in future systems. Prediction will need to be further improved to account for moving objects (ugh).
				
				if d: #there has been a collision
				#between k and velocity at d
					self.velocity = flip((-self.velocity[0], -self.velocity[1]), perp(k, d))
					break #don't keep testing for collisions if one already happened!
				
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
			stroke(min(1,self.Interface.bg[0]*1.8), min(1,self.Interface.bg[1]*1.8),min(1,self.Interface.bg[2]*1.8))
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
			
		#print(self.root_layer.sublayers)
		self.Interface.draw()
		
		#in-game menu
		if self.Interface.interface == "level":
			stroke(1,1,1,0)
			fill(1,1,1,0.6)
			stroke_weight(10)
			#fill(self.Interface.bg[0], self.Interface.bg[1], self.Interface.bg[2])
			rect(240,0,80,40)
			image('ionicons-ios7-pause-256', 280, 0, 40, 40)
			image('ionicons-loop-256',280,0,-40,40)
		#print self.Interface
		
		#print(len(self.Interface.guiSpace))
		for i in range(len(self.Interface.guiSpace)):
			element = self.Interface.guiSpace[i]
			tint(element[1].color[0], element[1].color[1], element[1].color[2])
			titleText = render_text(element[1].text, element[1].font, element[1].size)
			image(titleText[0], element[0].frame.x, element[0].frame.y, titleText[1][0], titleText[1][1])
			
			#print(self.Interface.guiSpace[i][0].frame.w-titleText[1].w)
			
			if not self.Interface.guiSpace[i][0].frame.w == titleText[1].w:
				self.Interface.guiSpace[i][0].frame.w = titleText[1].w
				self.Interface.guiSpace[i][0].frame.h = titleText[1].h
				#self.Interface.guiSpace[i][0].frame.x = element[2][0]-self.Interface.guiSpace[i][0].frame.w/2
				#self.Interface.guiSpace[i][0].frame.y = element[2][1]-self.Interface.guiSpace[i][0].frame.h/2
			#print(titleText[1])
				#self.setup()
			#print(titleText[1])
	
	def touch_began(self, touch):
		# Animate the layer to the location of the touch:
		if self.Interface.interface == "level":
			if 240<touch.location.x<320 and 0<touch.location.y<40:
				pass
			else:
				self.startx, self.starty = touch.location.x, touch.location.y
		if self.Interface.interface == "menu":
			if self.Interface.name == "menu1":
				if self.Interface.page == 0:
					self.Interface.page = 1
					#check new inter. vals for accuracy, especially with rects
					me = self.Interface.guiSpace[0][0]
					me.animate('frame', Rect(-100-me.frame.w/2, 284-me.frame.h/2, me.frame.w, me.frame.h), 1)
					me = self.Interface.guiSpace[1][0]
					me.animate('frame', Rect(160-me.frame.w/2,316-me.frame.h/2, self.Interface.guiSpace[1][0].frame.w, self.Interface.guiSpace[1][0].frame.h), 1)
					me = self.Interface.guiSpace[2][0]
					me.animate('frame', Rect(160-me.frame.w/2,242-me.frame.h/2, me.frame.w,me.frame.h), 1)
					#self.bganim = self.root_layer.animate('background', Color(0,0.62,1), 1)
					self.Interface.bg = (0,0.62,1)
					#go blue
				
				else:
					unhandled = True
					for element in self.Interface.guiSpace[1:]:
						if 0 <= touch.location.x-element[0].frame.x <= element[0].frame.w and 0 <= touch.location.y-element[0].frame.y <= element[0].frame.h:
							unhandled = False
							#here
							#check button title via text class then load level or menu by overriding interface
							if element[1].text == "Play":
								#embelish a bit (most recent level)
								#self.root_layer.animate('background', Color(0.2,0.2,0.2), 0.2)
								self.Interface = level1()
								self.position = self.Interface.spawn
							
					if unhandled:
						#REVERSE reverse
						
						me = self.Interface.guiSpace[0][0]
						me.animate('frame', Rect(160-me.frame.w/2, 284-me.frame.h/2, me.frame.w, me.frame.h), 1)
						me = self.Interface.guiSpace[1][0]
						me.animate('frame', Rect(420-me.frame.w/2,316-me.frame.h/2, self.Interface.guiSpace[1][0].frame.w, self.Interface.guiSpace[1][0].frame.h), 1)
						me = self.Interface.guiSpace[2][0]
						me.animate('frame', Rect(420-me.frame.w/2,242-me.frame.h/2, me.frame.w,me.frame.h), 1)
						#self.bganim = self.root_layer.animate('background', Color(1,1,1), 1)
						#go white
						self.Interface.bg = (1,1,1)
						
						self.Interface.page = 0
						
						#####
						
						
				#self.layer.animate('frame', new_frame, 1.0, curve=curve_bounce_out)
			
		#new_frame = Rect(x - 16, y - 16, 32, 32)
		#self.layer.animate('frame', new_frame, 1, curve=curve_bounce_out)
		# Animate the background color to a random color:
		#new_color = Color(random(), random(), random())
		#self.layer.animate('background', new_color, 1.0)
	
	def touch_moved(self, touch):
		if self.Interface.interface == "level":
			try:
				self.dragvector = (self.startx - touch.location.x, self.starty - touch.location.y)
			except:
				pass #prevent weird bugs
	
	def touch_ended(self, touch):
		if self.Interface.interface == "level":
			self.velocity = (self.velocity[0]+0.07*self.dragvector[0], self.velocity[1]+0.07*self.dragvector[1])
			self.dragvector = (0,0)

run(Game())