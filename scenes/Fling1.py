# https://gist.github.com/SamyBencherif/29b95a81de9e82c290d9
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
		
class Level():
	spawn = vector(0,0,32,32)
	collideSpace = [] #[]vector
	meshSpace = [] #[]vector
	tokenSpace = [] #[]vector
	def draw(self):
		stroke(1,1,1)
		stroke_weight(3)
		for v in self.meshSpace:
			line(v.x, v.y, v.x+v.w, v.y+v.h)
		for v in self.collideSpace:
			line(v.x, v.y, v.x+v.w, v.y+v.h)
	
level1 = Level()
level1.meshSpace = [vector(100,100, 100,50)]#[vector(100, 100, 200, 200), vector(100,100,0,100), vector(100, 100, -200, 300)]

#need a better way to go from visual to collider, account for square size
#level1.collideSpace = level1.meshSpace
for v in level1.meshSpace:
	angle = math.atan2(v.h, v.w)
	#add scaling here, or maybe just in render?
	level1.collideSpace.append(vector(v.x- 16*math.cos(angle), v.y+16*math.cos(angle), v.w+32*math.cos(angle), v.h))
	level1.collideSpace.append(vector(v.x- 16*math.cos(angle), v.y-16*math.cos(angle), v.w+32*math.cos(angle), v.h))
	#level1.collideSpace.append(vector(v.x-math.cos(angle)*16, v.y-math.cos(angle)*16, -32*math.sin(angle), 32*math.cos(angle)))
	#level1.collideSpace.append(vector(v.x+v.w+math.cos(angle)*16, v.y+v.h-math.cos(angle)*16,-32*math.sin(angle), 32*math.cos(angle)))
	
#level1.meshSpace += level1.collideSpace
#print(level1.meshSpace[0].x, level1.meshSpace[0].y)
#print (level1.collideSpace[0].x, level1.collideSpace[0].y)

level1.spawn.x = 200
level1.spawn.y = 500

class Game (Scene):
	def setup(self):
		self.level = level1
		#self.position = self.bounds.center()
		self.position = self.level.spawn
		self.dragvector = (0,0)
		self.velocity = (0,0)
		self.root_layer = Layer(self.bounds)
		self.drag = 0.99
		#add scaling here
		self.layer = Layer(Rect(self.position.x - 16, self.position.y - 16, 32, 32))
		self.layer.background = Color(1, 1, 1)
		#self.layer.image = 'Black_Square'
		self.root_layer.add_layer(self.layer)
	
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		background(0.5, 0.5, 0.8)
		
		#self.level.draw()
		
		#stroke_weight(3)
		#stroke(0.625,0.625,1)
		
		#scale level attributes up from my static display size to dynamic user screen size
		
		#TODO: optimize
		m = vector(self.position.x, self.position.y, self.velocity[0], self.velocity[1])
		#print(self.position.h)
		for k in self.level.collideSpace:
			#try:
			d = intersect(k, m)
			#except:
				#print("zero vect")
				#d = None
			#print(d)
			if d: #there has been a collision
				#between k and velocity at d
				self.velocity = flip((-self.velocity[0], -self.velocity[1]), perp(k, d))
				"""
				linAngle = math.atan2(k.h, k.w)+math.pi/2
				#print(linAngle)
				#angular bounce
				newAngle = linAngle + (linAngle - math.atan2(self.velocity[1], self.velocity[0]))
				newLen = (self.velocity[0]**2+self.velocity[1]**2)**.5
				self.velocity = (newLen*math.cos(newAngle), newLen*math.sin(newAngle))
				"""
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
		
		new_frame = Rect(self.position.x - 16, self.position.y - 16, 32, 32)
		self.layer.animate('frame', new_frame, 0)
		
		stroke_weight(3)
		stroke(0.625,0.625,1)
		line(self.position.x,self.position.y,self.position.x+self.dragvector[0],self.position.y+self.dragvector[1])
		
		import math

		self.angle = math.atan2(self.dragvector[1], self.dragvector[0])
		
		if not self.dragvector==(0,0):
		
			line(self.position.x+self.dragvector[0], self.position.y+self.dragvector[1], self.position.x+self.dragvector[0]+20*math.cos(self.angle+7*math.pi/8),self.position.y+self.dragvector[1]+20*math.sin(self.angle+7*math.pi/8))
		
			line(self.position.x+self.dragvector[0], self.position.y+self.dragvector[1], self.position.x+self.dragvector[0]+20*math.cos(self.angle-7*math.pi/8),self.position.y+self.dragvector[1]+20*math.sin(self.angle-7*math.pi/8))
			
		self.level.draw()
		
		self.root_layer.update(self.dt)
		self.root_layer.draw()
		
	
	def touch_began(self, touch):
		# Animate the layer to the location of the touch:
		self.startx, self.starty = touch.location.x, touch.location.y
		#new_frame = Rect(x - 16, y - 16, 32, 32)
		#self.layer.animate('frame', new_frame, 1, curve=curve_bounce_out)
		# Animate the background color to a random color:
		new_color = Color(random(), random(), random())
		#self.layer.animate('background', new_color, 1.0)
	
	def touch_moved(self, touch):
		self.dragvector = (self.startx - touch.location.x, self.starty - touch.location.y)
	
	def touch_ended(self, touch):
		self.velocity = (self.velocity[0]+0.07*self.dragvector[0], self.velocity[1]+0.07*self.dragvector[1])
		self.dragvector = (0,0)
		

run(Game())