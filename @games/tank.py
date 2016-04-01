# https://gist.github.com/GuyCarver/4141545
#Pythonista
# remote controlled tank without a game.  Haven't figured out the gameplay yet.
# Use remote app https://gist.github.com/959c9fba8e1e0c04f898 to control the tank.
# Work in progress.

from time import clock
from scene import *
from sound import *
from struct import *
from threading import Thread, Event
from math import sin, cos, pi, sqrt, acos, hypot, modf
from random import random, randint, shuffle, uniform, choice
import socket
import select

HOST = ''				 # Symbolic name meaning all available interfaces
PORT = 50007			  # Arbitrary non-privileged port

# Commonly used flag setes
READ_DATA = select.POLLIN | select.POLLPRI
READ_ONLY = READ_DATA | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT

pi2 = pi * 2 #360 deg rotation in radians.
hpi = pi / 2 #90 deg rotation in radians.
g_scale = 16 #global scale value for mobs.
numbullets = 1 #Number of bullets players may shoot at a time.
mgbulletcount = 8
mgrof = 0.1
bulletspeed = 1000 #Player bullet speed in pixles/second.
movesense = 2
movescale = .5
recoil = 32
recoildamp = recoil * 4
maxrpm = 0.2
tracksegs = 6
turnscale = .0125 #convert linear movement to angular radians/second.
expv = 32 #Maximum explosion velocity in pixles/second.
expav = pi #Maximum explosion angular velocity in radians/second.
expdur = .75 #Amount to reduce explosion alpha by per second.
blastdur = 2.5 #Amound to reduce blast alph by per second.
blastexp = 64 #Blast expansion rate in pixels/second.
deadtime = 5 #Seconds player stays dead.
remote = True #Set this to false to control the tank on the iPad.
screenrad = 100 #Distance from center of screen to a corner (calculated in Scene.setup())
debug = True  #Set to true to render waypoints and such.

sounds = ['Explosion_2', 'Hit_3', 'Drums_01', 'Explosion_5','Click_2','Ding_2']
images = ['Explosion']

playerverts = [Point(0, 1), Point(.5, .75), Point(.5, -.65), Point(0, -.75),
               Point(-.5, -.65), Point(-.5, .75),
               Point(.85, .75), Point(.85, -.65), Point(-.85, .75), Point(-.85, -.65)]
playersegs = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (1,6), (6,7), (7,2), (5,8), (8,9), (9,4)]
playermesh = (playerverts, playersegs)

turretsegs = [(0,1), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,2)]
turretverts = [Point(0, 1.5)]
turretmesh = (turretverts, turretsegs)

playerfilter = 1 #Player bullet collision ID.
aifilter = 2

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

# Set up the poller
poller = select.poll()
poller.register(server, READ_ONLY)

# Map file descriptors to socket objects
fd_to_socket = { server.fileno(): server, }

###-1 if < 0 otherwise 1
def sgn(val): return 1 if val >= 0 else -1
###squared length of given vector.
def lensq(vec): return (vec.x * vec.x + vec.y * vec.y)
###Dot product of p1, p2.
def dot(p1, p2): return p1.x * p2.x + p1.y * p2.y
###Center of segment p1-p2.
def center(p1, p2): return Point(p1.x + p2.x / 2, p1.y + p2.y / 2)
###Draw line between 2 points.
def drawline(p1, p2): line(p1.x, p1.y, p2.x, p2.y)

def dampen(val, d):
	###Return given velocity dampened by given amount not letting velocity change signs.
	s = sgn(val)
	val -= s * d
	if sgn(val) != s: val = 0 #If sign changed clamp at 0.
	return val

def normalize(pnt):
	###Normalize given Point in place and return the length.
	len = hypot(pnt.x, pnt.y)
	pnt.x /= len
	pnt.y /= len
	return len

def segvcircle(p1, p2, circle):
	###Check intersection of segment p1-p2 with circle.
	###circle is a Vector3, z = radius.
	segv = Point(p2.x - p1.x, p2.y - p1.y)
	#Get vector from p1 to circle.
	cp1v = Point(circle.x - p1.x, circle.y - p1.y)

	segvn = Point(*segv) #Make copy of vector from p1 to p2.
	l = normalize(segvn) # and normalize.

	sl = dot(cp1v, segvn) #Get distance from between line and circle.
	c = Point(*p1) #Start and segment point 1.
	#If off the end of the segment use the end point of the segment.
	if sl >= l: c = Point(*p2)
	elif sl > 0: #Move point on segment until segment of this point to circle
							 # is perpendicular to p1-p2 segment.
		c.x += segvn.x * sl
		c.y += segvn.y * sl
	#Return true if distnce from this point to circle is < radius of circle.
	return (c.distance(circle) < circle.z)

def addangle(a1, a2):
	###return a1 + a2 making sure the result is within 0-2pi.
	a1 += a2
	while a1 < 0: a1 += pi2
	while a1 > pi2: a1 -= pi2
	return a1

def rotpoint(a, p):
	###Rotate point in place by angle.
	c = cos(a)
	s = sin(a)
	x = p.x * c + p.y * s
	p.y = p.y * c - p.x * s
	p.x = x

def clippoint(pnt, bound):
	###Clip pnt in place to given bound.
	l = bound.left()
	r = bound.right()
	t = bound.top()
	b = bound.bottom()
	pnt.x = max(l, min(r, pnt.x))
	pnt.y = max(b, min(t, pnt.y))

def maketurret():
	p = Point(0, .45)
	turretverts.append(Point(*p))
	adj = pi2 / 8
	for i in xrange(8):
		rotpoint(adj, p)
		turretverts.append(Point(*p))			

class mob(object):
	###Base class representing a transformable vector graphics image.
	def __init__(self, pos, scn, mesh):
		object.__init__(self)
		self.scene = scn #Scene to which mob belogs.
		self.pos = Point(*pos)
		self.filter = 0 #Bullet ID.
		self.scale = g_scale #Scale of the mesh.
		self.color = Color(.4, .8, 1) #Color of the mesh.
		self.mesh = mesh
		self.points = [Point(*p) for p in mesh[0]] #Make copy of points for transform.
		self.angle = 0
		self.dotrans = True #If true transform the points on update.
		self.on = False #Start turned off.

	def reset(self):
		self.angle = 0 #Reset the heading.
		self.on = True #Turn on.

	def boundcheck(self, bound):
		###Check circle representing mob bound against given bound.
		if not self.on: return False
		x = bound.x - self.pos.x
		y = bound.y - self.pos.y
		dsq = x * x + y * y
		r = self.scale + bound.z #Radius of mob is scale * 1.
		return dsq <= r * r  #Collide if distance squared < square of radius sum.

	def offscreen(self):
		###Check if mob is off screen.
		s = self.scale
		s2 = 2 * s
		#Make rectangle around mob.
		r = Rect(self.pos.x - s, self.pos.y - s, s2, s2)
		return not self.scene.bounds.intersects(r)

	def transformpoints(self):
		###Transform points
		c = cos(self.angle)
		s = sin(self.angle)

		#Local function to transform point.
		def trans(p, d):
			d.x = (p.x * c + p.y * s) * self.scale + self.pos.x
			d.y = (p.y * c - p.x * s) * self.scale + self.pos.y

		#Loop through points and transform into destination of self.points
		for i, p in enumerate(self.mesh[0]):
			trans(p, self.points[i])

	def draw(self):
		###If on draw the mob.
		if self.on:
			stroke(*self.color)
			stroke_weight(1)
			if self.dotrans: self.transformpoints()
			for p0, p1 in self.mesh[1]:	#Draw each segment.
				drawline(self.points[p0], self.points[p1])

	###Turn off.
	def kill(self): self.on = False

class Flash(object):
	###Object to represent an explosion consisting of the exploded
	### mesh segments and a blast circle.
	def __init__(self, pr):
		self.color = Color(1.00, 1.00, 1.00)
		p = Point(-8, -8)
		self.frame = Rect(p.x + pr[0].x, p.y + pr[0].y, 16, 16)
		
	def update(self, dt):
		###Update explosion and return true when off.
		on = self.color.a > 0 #On as long as alpha isn't 0.
		if on:
			self.color.a = max(0, self.color.a - 4.0 * dt)
		return not on

	def draw(self):
		###Draw the explosion.
		fill(0,0,0,0) #No fill color.
		if self.color.a:
			tint(*self.color)
			image(images[0], *self.frame)
			
class explosion(object):
	###Object to represent an explosion consisting of the exploded
	### mesh segments and a blast circle.
	def __init__(self, mob):
		object.__init__(self)
		c = mob.color
		self.pos = Point(*mob.pos)
		self.alpha = 1
		self.color = Color(c.r, c.g, c.b, 1)
		self.angle = mob.angle
		self.blast = 4 #Stroke weight of blast circle.
		numsegs = len(mob.mesh[1])

		def make(index):
			###Make and explosion segment from the given segment index.
			###Returns a Tuple of Vector3 for point and angle, vector of segment, Vector3 of velocities).
			xv = uniform(-expv, expv) #Set random x,y velocities.
			yv = uniform(-expv, expv) #random() * expv * 2 - expv
			av = uniform(-expav, expav) #Set random angular velocity.
			i0, i1 = mob.mesh[1][index] #Get point indices for this segment.
			p0 = mob.points[i0] #Get point 0.
			p1 = Point(*mob.points[i1]) #Get copy of point 1.
			p1.x -= p0.x #Convert point 1 into vector to point1 from point0.
			p1.y -= p0.y
			return (Vector3(p0.x,p0.y,0), Point(p1.x, p1.y), Vector3(xv, yv, av))

		#Make list of segments representing exploded mesh.
		self.segs = [make(i) for i in xrange(numsegs)]
		set_volume(0.5)
		play_effect(sounds[3]) #Play explosion mesh.

	def update(self, dt):
		###Update explosion and return true when off.
		on = self.color.a > 0 #On as long as alpha isn't 0.
		if on:
			self.color.a = max(0, self.color.a - expdur * dt)
			self.alpha = max(0, self.alpha - blastdur * dt)
			self.blast += blastexp * dt
			for p0, _, v in self.segs:
				p0.x += v.x * dt
				p0.y += v.y * dt
				p0.z = addangle(p0.z, v.z * dt)
		return not on

	def draw(self):
		###Draw the explosion.
		fill(0,0,0,0) #No fill color.
		if self.alpha:
			width = self.alpha * 32 #The stroke width is % of 32 pixels.
			asq = self.alpha * self.alpha
			#Red alwasy 1, green = 1.5 * alpha, blue = 1 * alpha squared.
			#This will make the color animate from white to yellow to orange.
			stroke(1,1.5 * self.alpha,1 * asq, self.alpha)
			stroke_weight(width)
			x = self.pos.x - self.blast #Get lower left corner of circle.
			y = self.pos.y - self.blast
			wh = self.blast * 2 #Diameter.
			ellipse(x, y, wh, wh) #Draw the explosion circle.

		stroke(*self.color)
		stroke_weight(1)
		#Now draw the segments.
		for p0, p1d, v in self.segs:
			p1 = Point(p1d.x, p1d.y)
			rotpoint(p0.z, p1) #Rotate the direction by the angle.
			p1.x += p0.x #p1 = p0 + direction.
			p1.y += p0.y
			drawline(p0, p1)

class bullet(object):
	###Object representing a shot bullet.
	def __init__(self, owner):
		object.__init__(self)
		self.owner = owner #Owner of this bullet.
		self.pos = Point(0,0)
		self.vel = Point(0,0)
		self.color = Color(1, 0.7, 0.7)
		self.life = 0 #Current life of the bullet.
		self.speed = bulletspeed
		self.size = 2
		self.lifespan = .5 #Maximum life span of bullet in seconds.

	###Return filter ID of the owner of this bullet.
	def getfilter(self): return self.owner.filter

	def turnon(self, pos, vel):
		###Turn the bullet on.
		self.life = self.lifespan #Reset the life span.
		self.pos = pos
		self.vel.x = vel.x * self.speed
		self.vel.y = vel.y * self.speed

	def update(self, scn, dt):
		###Update bullet and return true when turned off.
		if self.life: #If any life left.
			self.life = (max(0, self.life - dt)) #Reduce life.
			if self.life: #If still on.
				prev = Point(*self.pos)
				self.pos.x += self.vel.x * dt
				self.pos.y += self.vel.y * dt
				#Check segment representing bullet traversal against mobs in scene.
				if scn.checkbullet(prev, self.pos, self.owner):
					self.life = 0 #Hit something so turn off.
			if not self.life:
				self.shotdone()
				return True
		return False
		
	def shotdone(self):
		self.owner.shotcount -= 1 #reduce shot count on owner if bullet turned off.

	def draw(self):
		###Draw bullet if on.
		if self.life:
			stroke(*self.color)
			stroke_weight(4)
			x1 = self.pos.x
			x2 = x1 + self.size
			y1 = self.pos.y
			y2 = y1 + self.size
			line(x1, y1, x2, y2)

class mgbullet(bullet):
	def __init__(self, owner):
		bullet.__init__(self, owner)
		self.color = Color(1.00, 0.44, 0.81)
		self.speed = bulletspeed * 1.5
		self.lifespan = .65 #Maximum life span of bullet in seconds.
		self.size = 1

	def shotdone(self):
		self.owner.mgshotcount -= 1 #reduce shot count on owner if bullet turned off.
		
class machine(mob):
	###Base class for player and AI machines.  You will note some
	### features that are not used by all machines.  They are here
	### just in case.  For instance making robbers shoot.
	def __init__(self, pos, filter, scn, mesh, bulletcount):
		mob.__init__(self, pos, scn, mesh)
		self.filter = filter #Set bullet ID.
		self.brk = 2 #Break amount in pixels/second.
		self.brka = pi * 2 #Angular break amount int rads/second.
		self.shotcount = 0 #Number of shots.
		#Create bullets.
		self.bullets = [bullet(self) for i in xrange(bulletcount)]
		self.shoot = sounds[0] #Set shooting sound.
		self.shootv = 0.6 #Shot sound volume.

	def reset(self):
		###Reset the mob.
		mob.reset(self)
		self.avel = 0
		self.vel = Point(0, 0)
		self.wrap = True  #Wrap mob around on screen as opposed to cliping on edges.

	def fire(self):
		###Shoot a bullet.
		if self.on and self.shotcount < len(self.bullets):
			for b in self.bullets:
				if not b.life: #Find unused bullet.
					b.turnon(*self.shotpos())
					self.shotcount += 1
					set_volume(self.shootv)
					play_effect(self.shoot)
					self.scene.activebullets.append(b) #Add bullet to scene.
					return

	def update(self, dt):
		###Update machine.
		if self.on:
			v = Point(*self.vel)
			rotpoint(self.angle, v)
			self.pos.x += v.x * dt #Add velocity to position.
			self.pos.y += v.y * dt
			if self.wrap: #If wraping on screen then do so.
				sz = self.scene.size

				if self.pos.x > sz.w:
					self.pos.x -= sz.w
				elif self.pos.x < 0:
					self.pos.x += sz.w

				if self.pos.y > sz.h:
					self.pos.y -= sz.h
				elif self.pos.y < 0:
					self.pos.y += sz.h
			#Adjust direction by angular velocity.
			self.angle = addangle(self.angle, self.avel * dt)

class player(machine):
	###Machine to represent a player.
	def __init__(self, pos, scn, dir):
		machine.__init__(self, pos, playerfilter, scn, playermesh, numbullets)
		self.color = Color(0.40, 1.00, 1.00)
		self.dir = dir #+/-1.
		self.startpos = Point(*pos)
		self.turret = [Point(*p) for p in turretmesh[0]] #Make copy of points for transform.
		self.mg = [Point(*p) for p in turretmesh[0]] #Make copy of points for transform.
		self.mgbullets = [mgbullet(self) for i in xrange(mgbulletcount)]
		self.mgshotcount = 0
		self.mgshoot = sounds[2]
		self.shoot = sounds[0] #Set shooting sound.
		self.setcontrols()
		self.settrack()
		self.reset()

	def setcontrols(self):
		w = self.scene.size.w
		h = self.scene.size.h
		w3 = w / 5 #1/5th Screen width.
		w6 = w3 / 2 #1/10th Screen width.

		self.lmoverect = Rect(w - w3, w3, w3, w6) #Set movement button rectangle.
		self.rmoverect = Rect(w - w3, h - w3 - w6, w3, w6) #Set fire button rectangle.
		self.tmoverect = Rect(0, w3 * 2, w6, h - w3 * 2.5) #Set fire button rectangle.
		self.mgmoverect = Rect(0, w6, w6, w3) #Set fire button rectangle.
		self.lmovepos = self.lmoverect.center()
		self.rmovepos = self.rmoverect.center()
		self.tmovepos = self.tmoverect.center()
		self.mgmovepos = self.mgmoverect.center()

	def settrack(self):
		p0 = Point(*self.points[1])
		p1 = Point(*self.points[2])
		p0.y *= self.scale
		p1.y *= self.scale
		
		h = p0.y - p1.y
		self.tlink = h / (tracksegs)
		self.tracklen = h
		self.ltrackpos = 0.0
		self.rtrackpos = 0.0

	def reset(self):
		###Reset the player to original position.
		machine.reset(self)
		self.dead = 0
		self.lvel = 0
		self.rvel = 0
		self.lveltarget = 0
		self.rveltarget = 0
		self.turretvel = 0
		self.turretvelt = 0
		self.turreta = 0
		self.mga = 0
		self.mgvel = 0
		self.mgfire = 0
		self.mgrate = 0
		self.rpm = 0
		self.pos.x = self.startpos.x
		self.pos.y = self.startpos.y
		self.vel.y = self.scale * 8 #Start out with a velocity to move onto screen.
		self.angle = -hpi
		self.destangle = self.angle

	def transformpoints(self):
		###Transform turret points.
		machine.transformpoints(self)

		a = self.angle + self.turreta
		c = cos(a)
		s = sin(a)

		#Local function to transform point.
		def trans(p, d):
			d.x = (p.x * c + p.y * s) * sc + self.pos.x
			d.y = (p.y * c - p.x * s) * sc + self.pos.y

		sc = self.scale
		#Loop through points and transform into destination of self.points
		for i, p in enumerate(turretmesh[0]):
			trans(p, self.turret[i])

		sc *= .25
		mgoff = Point(sc, 0)
		rotpoint(a, mgoff)
		a += self.mga
		c = cos(a)
		s = sin(a)

		for i, p in enumerate(turretmesh[0]):
			mgp = self.mg[i]
			trans(p, mgp)
			mgp.x += mgoff.x
			mgp.y += mgoff.y

	def firemg(self, dt):
		###Shoot a bullet.
		if self.on and self.mgshotcount < len(self.mgbullets):
			if self.mgrate <= 0:
				for b in self.mgbullets:
					if not b.life: #Find unused bullet.
						b.turnon(*self.mgshotpos())
						self.mgshotcount += 1
						set_volume(self.shootv)
						play_effect(self.mgshoot)
						self.scene.activebullets.append(b) #Add bullet to scene.
						self.mgrate = mgrof
						return
			else:
				self.mgrate = max(0, self.mgrate - dt)

	def mgshotpos(self):
	###Get screen position and shot direction.
		p = Point(*self.mg[0]) #Shot comes out of point 0.
		p0 = self.mg[1]
		v = Point((p.x - p0.x) / self.scale, (p.y - p0.y) / self.scale)
		return (p, v)

	def shotpos(self):
	###Get screen position and shot direction.
		p = Point(*self.turret[0]) #Shot comes out of point 0.
		p0 = self.turret[1]
		v = Point((p.x - p0.x) / self.scale, (p.y - p0.y) / self.scale)
		rc = Point(*v)
		rotpoint(-self.angle, rc)
		self.vel.x -= rc.x * recoil
		self.vel.y -= rc.y * recoil
		sp = (p, v)
		self.scene.flash(sp)
		return sp

	def draw(self):
		machine.draw(self)

		d = Point(*self.points[1])
		p1 = Point(*self.points[2])
		p2 = Point(*self.points[7])
		d.x -= p1.x
		d.y -= p1.y
		normalize(d)
		n = Point(*d)
		tlv = Point(d.x * self.tracklen, d.y * self.tracklen)
		d.x *= self.tlink
		d.y *= self.tlink
			
		def drawtrack(tp, pp1, pp2):
			tpv = Point(n.x * tp, n.y * tp)
			pp1.x += tpv.x
			pp1.y += tpv.y
			pp2.x += tpv.x
			pp2.y += tpv.y
			for i in xrange(tracksegs):
				tp += self.tlink
				pp1.x += d.x
				pp1.y += d.y
				pp2.x += d.x
				pp2.y += d.y
				if tp >= self.tracklen:
					tp -= self.tracklen
					pp1.x -= tlv.x
					pp1.y -= tlv.y
					pp2.x -= tlv.x
					pp2.y -= tlv.y
				drawline(pp1, pp2)

		stroke(1.00, 1.00, 0.00)			
		drawtrack(self.rtrackpos, p1, p2)
		p1 = Point(*self.points[4])
		p2 = Point(*self.points[9])

		drawtrack(self.ltrackpos, p1, p2)
		
		stroke(0.40, 1.00, 0.80)
		for p0, p1 in turretmesh[1]:	#Draw each segment.
			drawline(self.turret[p0], self.turret[p1])

		stroke(1.00, 0.00, 0.00)
		for p0, p1 in turretmesh[1]:	#Draw each segment.
			drawline(self.mg[p0], self.mg[p1])

	def kill(self):
		###Kill the player.
		mob.kill(self)
		self.dead = deadtime #Start dead timer.

	def move(self, dt):
		###Move the player.
		self.avel = (self.lvel - self.rvel) * turnscale
		
		rp = Point(self.mesh[0][7].x * self.scale, 0)
		lp = Point(self.mesh[0][9].x * self.scale, 0)
		rotpoint(self.avel, rp)
		rotpoint(self.avel, lp)
		rp.y += self.vel.y
		lp.y += self.vel.y

		def calctrackpos(tp):
			while tp < 0: tp += self.tracklen
			while tp >= self.tracklen: tp -= self.tracklen
			return tp
				
		self.rtrackpos = calctrackpos(self.rtrackpos + rp.y * dt)
		self.ltrackpos = calctrackpos(self.ltrackpos + lp.y * dt)
		
		def calcvel(vt, cv, brk):
			v = vt - cv
			if v:
				cv += v * brk * dt
				if v < 0:
					if cv < vt: cv = vt
				elif cv > vt: cv = vt
			return cv
						
		self.lvel = calcvel(self.lveltarget, self.lvel, 4)
		self.rvel = calcvel(self.rveltarget, self.rvel, 4)
		destv = (self.rvel + self.lvel) * 0.5
		self.vel.y = calcvel(destv, self.vel.y, self.brk)
		self.vel.x = dampen(self.vel.x, recoildamp * dt)
		self.turretvel = calcvel(self.turretvelt, self.turretvel, pi)
		self.turreta = addangle(self.turreta, self.turretvel * dt)
		self.mga = addangle(self.mga, self.mgvel * dt)

	def udengine(self, dt):
		self.rpm = max(0, self.rpm - dt)
		if not self.rpm:
			v = max(abs(self.lvel), abs(self.rvel))
			self.rpm = max(0.05, 0.4 - v * 0.004)
			set_volume(0.1)
			play_effect(sounds[4])
			
	def update(self, dt):
		if self.on: #If on then update.
			self.move(dt)
			machine.update(self, dt)
#			self.udengine(dt)
			if self.mgfire > 0:
				self.firemg(dt)
			else: self.mgfire = 0
		else: #Death of player is different from killer which uses state functions
					# simply to show another way of doing it.  I prefer states.
			self.dead -= dt
			if self.dead <= 0: #As soon as dead time up reset.
				self.reset()

	def touch_began(self, touch):
		#Check left/right button pressed, return true if handled.
		if self.on:
			tl = touch.location
			if tl in self.lmoverect: #If movement rectangle touched.
				self.lveltarget = (self.lmovepos.x - touch.location.x)
				return True
			if tl in self.rmoverect: #If fire rectangle touched.
				self.rveltarget = (self.rmovepos.x - touch.location.x)
				return True
			if tl in self.tmoverect:
				self.turretvelt = (self.tmovepos.y - touch.location.y) * turnscale
				return True
			if tl in self.mgmoverect:
				self.mgvel = (self.mgmovepos.y - touch.location.y) * turnscale
				self.mgfire += 1
				return True	
		return False

	def touch_moved(self, touch):
		if self.on:
			tl = touch.location
			if tl in self.lmoverect: #If movement rectangle touched.
				self.lveltarget = (self.lmovepos.x - touch.location.x )
				return True

			tpl = touch.prev_location
			if tpl in self.lmoverect: #If previous location was in movement rectangle then stop movement.
				return True

			if tl in self.rmoverect: #If fire rectangle touched calculate anguler velocity.
				self.rveltarget = (self.rmovepos.x - touch.location.x)
				return True
				
			if tpl in self.rmoverect: #If previous location was in movement rectangle then stop movement.
				return True

			if tl in self.tmoverect: #If fire rectangle touched calculate anguler velocity.
				self.turretvelt = (self.tmovepos.y - touch.location.y) * turnscale
				return True

			if tpl in self.tmoverect: #If previous location was in movement rectangle then stop movement.
				return True

			if tl in self.mgmoverect: #If fire rectangle touched calculate anguler velocity.
				self.mgvel = (self.mgmovepos.y - touch.location.y) * turnscale
				return True

			if tpl in self.mgmoverect: #If previous location was in movement rectangle then stop movement.
				self.mgfire -= 1
				return True

		return False

	def touch_ended(self, touch):
		#Touch ends.
		if self.on:
			tl = touch.location
			if tl in self.lmoverect: #If no longer touching movement button decrement control count.
				self.lveltarget = 0
				return True
			if tl in self.rmoverect: #If no longer touching movement button decrement control count.
				self.rveltarget = 0
				return True
			if tl in self.tmoverect: #If no longer touching movement button decrement control count.
				self.turretvelt = 0
				self.fire()
				return True
			if tl in self.mgmoverect: #If no longer touching movement button decrement control count.
				self.mgvel = 0
				self.mgfire -= 1

		return False

class MyScene(Scene):
	###Main scene.
	def setup(self):
		### This will be called before the first frame is drawn.
		global screenrad
		maketurret()
		pos = self.bounds.center()
		cp = Point(*pos)
		pos.x = 0
		w = self.size.w
		h = self.size.h
		screenrad = sqrt(lensq(Point(w, h))) * .5 #Set screen radius.
		self.pl = []
		plr = player(pos, self, 1.0) #Create player 1.
		self.pl.append(plr)
		
		self.activebullets = [] #Array of active bullets.
		self.explosions = [] #Array of active explosions.
		self.controlalpha = 0.45 #Control rectangle alpha.
		self.state = self.run
		self.gameovertxt = render_text('You Tanked!', 'Copperplate', 32)
		self.pausetxt = render_text('Pause', 'Copperplate', 28)
		c = self.bounds.center()
		hh = self.pausetxt[1].w * .5
		self.pauserect = Rect(c.x - hh, 0, hh * 2, self.pausetxt[1].h)

		for s in sounds: load_effect(s) #pre-load sound effects.
		for image in images: load_image(image)
		
	def checkbullet(self, p1, p2, owner):
		###Check bullet collision, return true if hit something.
		hit = False
		def checkcol(amob):
			###Local function to
			if amob.on:
				circle = Vector3(amob.pos.x, amob.pos.y, amob.scale)
				if segvcircle(p1, p2, circle): #If circle hit then create an explosion.
					self.explosions.append(explosion(amob))
					amob.kill() #Kill the hit object.
					return True
			return False

		#If not a player ID then check player collisions.
		if owner.filter != playerfilter:
			for p in self.pl:
				hit |= checkcol(p)
		elif owner.filter != aifilter: #If not AI ID.
			pass

		return hit

	def flash(self, sp):
		self.explosions.append(Flash(sp))

	def getremotedata(self):
		events = poller.poll(0) #read data

		lastdata = None
		lastts = 0

		for fd, flag in events:
			# Retrieve the actual socket from its file descriptor
			s = fd_to_socket[fd]
			
			# Handle inputs
			if flag & READ_DATA:
				data, addr = s.recvfrom(32)
				ts = unpack_from('i', data)
				if ts > lastts:
					lastdata = data
					lastts = ts

		return lastdata
		
	def updateremote(self, plr):
		data = self.getremotedata()
		if data:
			tstamp, lvel, rvel, tvel, mgvel, shoot, mgon, psd = unpack('iffff???', data)
			plr.lveltarget = lvel
			plr.rveltarget = rvel
			plr.turretvelt = tvel
			plr.mgvel = mgvel
			plr.mgfire = int(mgon)
			if shoot:
				plr.fire()
			spsd = (self.state == self.paused)
			if (psd and not spsd) or (spsd and not psd):
				self.togglepause()

	def update(self, dt):
		###Update the scene.
		if debug:
			self.t0 = clock()

		#if no screen touches reset control counters for safety (they can get out of sync).
		if len(self.touches) == 0:
			for p in self.pl:
				p.control = 0
		for p in self.pl: #Update players.
			p.update(dt)

		#Update active bullets.
		for b in self.activebullets:
			if b.update(self, self.dt):
				self.activebullets.remove(b)
		#Update active explosions.
		for e in self.explosions:
			if e.update(dt):
				self.explosions.remove(e)

		if debug:
			self.t1 = clock()

	###Pause state does nothing.
	def paused(self):
		if remote:
			data = self.getremotedata()
			if data:
				tstamp, lvel, rvel, tvel, mgvel, shoot, mgon, psd = unpack('iffff???', data)
				if not psd:
					self.togglepause()
				
	def gameover(self):
		###Game over state.
		tint(0.00, 1.00, 0.00)
		c = self.bounds.center()
		s = self.gameovertxt[1]
		image(self.gameovertxt[0], c.x - (s.w / 2), c.y, *s)
		self.update(self.dt / 4)

	def run(self):
		###Main state.
		dt = min(0.1, self.dt)
		if remote:
			self.updateremote(self.pl[0])
		self.update(dt)

	def drawcontrols(self):
		###Draw control boxes.
		if not remote and self.controlalpha:
			fill(0,0,0,0)
			stroke(0, 0, .5, self.controlalpha)
			stroke_weight(2)
			for p in self.pl:
				rect(*p.lmoverect)
				rect(*p.rmoverect)
			stroke(.5, 0, .5, self.controlalpha)
			for p in self.pl:
				rect(*p.tmoverect)
				rect(*p.mgmoverect)

	def drawscore(self):
		###Draw the score and pause text.
		tint(1,0,0)
		c = self.bounds.center()
#		s = self.scoretxt[1]
#		image(self.scoretxt[0], c.x - (s.w / 2), self.size.h - s.h, *s)
		clr = Color(1,1,0) if self.state == self.paused else Color(0.80, 0.40, 1)
		if debug: #In debug draw timing text.
			tmg = int((self.dt) * 1000.0)
			st = str(tmg)
			text(st, x=20, y=20, alignment=9)
		tint(*clr)
		s = self.pausetxt[1]
		image(self.pausetxt[0], c.x - (s.w / 2), 0, *s)

	def draw(self):
		###Draw all objects in the scene.
		self.state() #Update state.
		background(0, 0, 0)
		self.drawscore()
		self.drawcontrols()

		for p in self.pl: p.draw()
		for b in self.activebullets: b.draw()
		for e in self.explosions: e.draw()

	def togglepause(self):
		play_effect(sounds[5])
		if self.state == self.paused:
			self.state = self.prevstate
		else:
			self.prevstate = self.state
			self.state = self.paused
						
	def checkpause(self, loc):
		###Check to see if pause button pressed.
		if loc in self.pauserect:
			self.togglepause()

	def touch_began(self, touch):
		###Handle touch events.
		if not remote:
			for p in self.pl:
				if p.touch_began(touch):
					return

	def touch_moved(self, touch):
		###Handle touch move events.
		if not remote:
			for p in self.pl:
				if p.touch_moved(touch):
					return

	def touch_ended(self, touch):
		###Handle touch end events.
		if not remote:
			for p in self.pl:
				if p.touch_ended(touch):
					return
		self.checkpause(touch.location) #Check for pause button press.

run(MyScene(), LANDSCAPE)