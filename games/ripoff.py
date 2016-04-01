# https://gist.github.com/GuyCarver/4115763
# ----------------------------------------------------------------------
# Copyright (c) 2012, Guy Carver
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#
#     * The name of Guy Carver may not be used to endorse or promote products # derived#
#       from # this software without specific prior written permission.#
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# FILE    ripoffv3.py
# BY      Guy Carver
# DATE    11/19/2012 06:16 PM
#----------------------------------------------------------------------

from time import clock
from scene import *
from sound import *
from threading import Thread, Event
from math import sin, cos, pi, sqrt, acos, hypot, modf
from random import random, randint, shuffle, uniform, choice

pi2 = pi * 2 #360 deg rotation in radians.
hpi = pi / 2 #90 deg rotation in radians.
g_scale = 16 #global scale value for mobs.
numcrates = 9 #Number of crates to start with.
cratespacing = 45 #Space between crates in rows and columns.
numbullets = 5 #Number of bullets players may shoot at a time.
aibulletspeed = 500 #Speed of AI bullets in pixels/second.
aibulletlife = .5 #Life time of AI bullets in seconds.
bulletspeed = 1000 #Player bullet speed in pixles/second.
movesense = 2
movescale = 2
turnscale = .05 #convert linear movement to angular radians/second.
uadj = pi / 16 #maximum random amount to adjust angular velocity by when unstable (on a crate)
expv = 32 #Maximum explosion velocity in pixles/second.
expav = pi #Maximum explosion angular velocity in radians/second.
expdur = .75 #Amount to reduce explosion alpha by per second.
blastdur = 2.5 #Amound to reduce blast alph by per second.
blastexp = 64 #Blast expansion rate in pixels/second.
deadtime = 5 #Seconds player stays dead.
screenrad = 100 #Distance from center of screen to a corner (calculated in Scene.setup())
tetherlen = 32 #Length of tether from robber to crate.
maxkillers = 4 #Maximum number of killer AI mobs.
firedelay = .5 #Delay between shots by killers when zeroed in.
robbercount = 6 #Number of robbers.
killerinterval = 4 #Waves between killer addition.
killerdowntime = 5 #Seconds killer remains dead before re-spawning.
killervel = 1.25 #Velocity scalar.
velbase = 100.0 #Base velocity for all AI.
velscale = 1.0 / 100.0 #Velocity increase per wave for robbers and killers.
mt = False #True = multi-thread AI update.  Actually slows things down a bit.
debug = False #Set to true to render waypoints and such.

crateverts = [Point(-.5, 0), Point(0, .75), Point(.5, 0), Point(0, -.75)]
cratesegs = [(0,1), (1,2), (2,3), (3,0), (0,2)]
cratemesh = (crateverts, cratesegs)

playerverts = [Point(0, .75), Point(1, 0), Point(.75, -.5), Point(.5, -.25),
               Point(-.5,-.25), Point(-.75,-.5), Point(-1, 0)]
playersegs = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,0)]
playermesh = (playerverts, playersegs)

robberverts = [Point(0, 1), Point(.5, .25), Point(.5, -.25), Point(0, -.75),
               Point(-.5, -.25), Point(-.5, .25)]
robbersegs = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0, 3)] #(1,5), (2,4)]
robbermesh = (robberverts, robbersegs)

killerverts = [Point(0,1), Point(.35,0), Point(.5, -.75), Point(0,0),
               Point(-.5,-.75), Point(-.35,0)]
killersegs = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0)]
killermesh = (killerverts, killersegs)

sounds = ['Laser_6', 'Laser_3', 'Hit_3', 'Explosion_5','Clank','Ding_2']

#Waypoint list for robbers.
#tuple of distance from screen center, angle relative to current position in radians, min,max % of velbase.
pathrange = [(.85, pi, Point(.8, .6)), (.5, hpi, Point(.6, .5)), (.25, hpi / 2, Point(.5, .3)), (0, 0, Point(.3, .02)), (1.5, pi, Point(.6, .3))]
exitwp = len(pathrange) - 1 #Index for the exit waypoint.
pickupwp = exitwp - 1 #Index of the crate pickup waypoint.
wpskipchance = 0.1 #% chance of skipping an approach waypoint.
wpskipfactor = 0.01 #Amount to add to wpskipchance per wave.

playerfilter = 1 #Player bullet collision ID.
aifilter = 2 #AI bullet collision ID.

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

def deltaangle(a0, a1):
	###Return shortest angle in radians between a1 and a0.
	### Result will -pi < delta < pi.
	a = a1 - a0
	b = abs(a)
	c = pi2 - b #Get rotation in oppisite direction.
	if b < c: return a #if 1st rotation is shorter then return it.
	else: return c * -sgn(a) #Otherwise return 2nd rotation setting the sign to opposite of 1st rotation.

def anglefromvector(vect):
	#Return Tuple (radian rotation, vect length) represented by given vector.
	len = hypot(vect.x, vect.y) #sqrt(lensq(vect))
	if len > 0: #If not 0 length.
		a = acos(vect.y / len) #Get angle from cos.
		#If x negative then angle is between pi-2pi
		if vect.x < 0: a = pi2 - a
	else: a = 0
	return (a, len)

def dampen(val, d):
	###Return given velocity dampened by given amount not letting velocity change signs.
	s = sgn(val)
	val -= s * d
	if sgn(val) != s: val = 0 #If sign changed clamp at 0.
	return val

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

		###Make and explosion segment from the given segment index.
		###Returns a Tuple of Vector3 for point and angle, vector of segment, Vector3 of velocities).
		def make(index):
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

class crate(mob):
	###Mob rebresenting a crate the robbers will attempt to steal.
	def __init__(self, pos, scn):
		mob.__init__(self, pos, scn, cratemesh)
		self.color = Color(0.80, 0.80, 0.20)
		self.reset()

	def reset(self):
		mob.reset(self)
		self.targeted = 0 #No robbers are targeting.
		self.tethered = None #No robber is tethered to the crate.
		self.dotrans = False #Don't transform the points each frame.
		self.transformpoints() #Transform the points 1 time.

	def kill(self):
		###Kill the crate.
		mob.kill(self)
		self.scene.killcrate(self) #Remove the create from the scene.
		set_volume(0.5)
		play_effect(sounds[4])

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
		self.lifespan = 1 #Maximum life span of bullet in seconds.

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
				self.owner.shotcount -= 1 #reduce shot count on owner if bullet turned off.
				return True
		return False

	def draw(self):
		###Draw bullet if on.
		if self.life:
			stroke(*self.color)
			stroke_weight(4)
			x1 = self.pos.x
			x2 = x1 + 2
			y1 = self.pos.y
			y2 = y1 + 2
			line(x1, y1, x2, y2)

class machine(mob):
	###Base class for player and AI machines.  You will note some
	### features that are not used by all machines.  They are here
	### just in case.  For instance making robbers shoot.
	def __init__(self, pos, filter, scn, mesh, bulletcount):
		mob.__init__(self, pos, scn, mesh)
		self.filter = filter #Set bullet ID.
		self.brk = 200 #Break amount in pixels/second.
		self.brka = pi * 2 #Angular break amount int rads/second.
		self.shotcount = 0 #Number of shots.
		#Create bullets.
		self.bullets = [bullet(self) for i in xrange(bulletcount)]
		self.shoot = sounds[0] #Set shooting sound.
		self.shootv = 0.6 #Shot sound volume.

	###Reset the mob.
	def reset(self):
		mob.reset(self)
		self.avel = 0
		self.vel = Point(0, 0)
		self.wrap = True  #Wrap mob around on screen as opposed to cliping on edges.

	###Apply breaks to liner velocity.
	def slowdown(self, dt): self.vel.y = dampen(self.vel.y, self.brk * dt)

	###Get screen position and shot direction.
	def shotpos(self):
		p = Point(*self.points[0]) #Shot comes out of point 0.
		v = Point((p.x - self.pos.x) / self.scale, (p.y - self.pos.y) / self.scale)
		return (p, v)

	###Shoot a bullet.
	def fire(self):
		if self.on and self.shotcount < len(self.bullets):
			for b in self.bullets:
				if not b.life: #Find unused bullet.
					b.turnon(*self.shotpos())
					self.shotcount += 1
					set_volume(self.shootv)
					play_effect(self.shoot)
					self.scene.activebullets.append(b) #Add bullet to scene.
					return

	###Update machine.
	def update(self, dt):
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

class aimachine(machine):
	###Base class for the AI controlled machines.
	def __init__(self, scn, mesh, numbullets):
		machine.__init__(self, Point(0,0), aifilter, scn, mesh, numbullets)
		self.on = False #Start turned off.
		self.brka = 0 #No angular velocity break.

	def reset(self, pos, angle):
		machine.reset(self)
		self.wrap = False #Don't wrap AI mobs on screen.
		self.pos = pos
		self.angle = angle
		self.minvel = 0
		self.maxvel = 0
		self.wp = Point(0,0)
		self.wpn = Point(0,0)
		self.nextwaypoint() #Set 1st waypoint.

	###Return base velocity adjust by the wave count.
	def basevel(self): return velbase + (velbase * float(self.scene.wave) * velscale)

	def updatevels(self, dt):
	###Update the linear and angular velocities.
		vect = Point(*self.wp)
		vect.x -= self.pos.x
		vect.y -= self.pos.y
		a, l = anglefromvector(vect) #Get angle, distance to target.
		self.avel = deltaangle(self.angle, a) #Get delta angle to target.
		self.vel = Point(0, max(self.minvel, min(self.maxvel, l))) #Set velocity based on target distance.

	def checkdest(self):
		###Check to see if we have reached target waypoint.
		delta = Point(self.pos.x - self.wp.x, self.pos.y - self.wp.y)
		l = lensq(delta)
		#If distance < minimum velocity.
		if l < (self.minvel * self.minvel):
			d = dot(delta, self.wpn) #See if we are on other side of waypoint normal.
			return d <= 0
		return False

	def update(self, dt):
		###Update the AI machine if on. return 1 if updated else 0.
		if self.on:
			self.state(dt) #Call the state function.
			machine.update(self, dt) #Call base update method.
			return 1
		return 0

class robber(aimachine):
	###Robber AI machine.
	def __init__(self, scn):
		aimachine.__init__(self, scn, robbermesh, 0)

	def reset(self, pos, angle, tgt):
		self.state = self.approachstate #Start with target approach state.
		self.wpindex = -1 #Start with waypoint index -1 so 1st index will be 0 when NextWaypoint is called.
		self.approacha = 0 #Approach angle of 0.
		self.target = tgt #Target crate.
		if tgt: tgt.targeted += 1
		aimachine.reset(self, pos, angle)

	def setexit(self)	:
		###Set exit state and tether to target crate.
		self.state = self.exitstate
		self.wrap = False
		tgt = self.target
		if not tgt.tethered: #If target not tethered then tether to it.
			b = Vector3(self.pos.x, self.pos.y, self.scale)
			if tgt.boundcheck(b): #Make sure in range of target before tethering.
				tgt.tethered = self
				tgt.dotrans = True #start crate updating transform as we are going to move it.
				return
		#if didn't tether then follow crate (Another robber is tethered to it).
		self.wp = tgt.pos #Reference target position and follow that.
											# If target moves so will our way point.
		self.state = self.followstate

	def done(self):
		###The robber has exited the screen so turn off.
		self.on = False
		#If tethered to a crate the kill the crate.
		if self.target and self.target.tethered is self:
			self.target.kill()

	def kill(self):
		###Kill the robber.
		mob.kill(self)
		tgt = self.target
		if tgt: #If targeting a create stop targeting.
			self.target = None
			tgt.targeted -= 1
			if tgt.tethered is self: #If pulling a crate then stop pulling.
				tgt.tethered = None
				tgt.dotrans = False #Make crate not update it's transforms as it is no longer moving.

	def pullcrate(self, dt):
		###Pull the crate.
		tgt = self.target
		if tgt and tgt.tethered is self:
			if tgt.offscreen(): #If target off screen then kill robber/crate.
				self.done()
			else: #Move crate.
				p = tgt.pos
				d = Point(self.pos.x - p.x, self.pos.y - p.y)
				dm = Point(abs(d.x) - tetherlen, abs(d.y) - tetherlen)
				if dm.x > 0:
					p.x += dm.x * sgn(d.x)
				if dm.y > 0:
					p.y += dm.y * sgn(d.y)
		elif self.offscreen(): #If robber off screen then stop it.
			self.done()

	#Get screen location of tether point on mesh.
	def tetherpos(self): return self.points[3] #Point 3 is tether point.

	def nextwaypoint(self):
		###Set next waypoint.
		self.wpindex += 1
		#Run chance of skipping waypoint but only up to pickup waypoint.
		while self.wpindex < pickupwp and (random() < self.scene.wpskipchance):
			self.wpindex += 1
		self.setwaypoint() #Set the waypoint position and normal.
		if self.wpindex == exitwp: #If we are at the exit waypoint change states.
			self.setexit()

	def setwaypoint(self):
		###Set the waypoint.
		if self.target:
			rad, da, vels = pathrange[self.wpindex]
			v = self.basevel()
			self.maxvel = vels.x * v #Set maximum/minimum velcoties as % of base velocity.
			self.minvel = vels.y * v
			#Adjust current approach angle by delta angle from next waypoint.
			self.approacha = addangle(self.approacha, uniform(-da, da))
			self.wp = Point(0, rad * screenrad)
			rotpoint(self.approacha, self.wp)
			self.wp.x += self.target.pos.x
			self.wp.y += self.target.pos.y
			if self.wpindex < exitwp: #don't clip exit waypoint as it takes us off screen.
				clippoint(self.wp, self.scene.bounds) #Clip point to screen.
			#Waypoint normal from vector of pos-wp.
			self.wpn = Point(self.pos.x - self.wp.x, self.pos.y - self.wp.y)
			normalize(self.wpn)

	def followstate(self, dt):
		###Watch target and if no longer tethered then tether to it.
		if not self.target.tethered: #If not tethered.
			self.wpindex = pickupwp #Re-run pickup waypoint.
			self.state = self.approachstate #Switch back to approach state.
			self.setwaypoint() #Set pickup waypoint.
		else:
			self.exitstate(dt) #Run exit state.

	def approachstate(self, dt):
		###Approach target through series of waypoins.
		if self.checkdest(): #Check if reached waypoint.
			self.nextwaypoint() #Next waypoint.
		self.updatevels(dt) #Update the velocities to get to waypoint.
		machine.update(self, dt)

	def exitstate(self, dt):
		self.updatevels(dt) #Update velocities to get to waypoint.
		self.pullcrate(dt) #Pull the crate if tethered.  NOTE: We could make a
											 # exitpull state and not have to check if tethered in pullcrate().

	def draw(self):
		###Draw the robber if on.
		if self.on:
			mob.draw(self)
			tgt = self.target
			#If tethered then draw tether line.
			if tgt and tgt.tethered is self:
				stroke(1,1,1,.5)
				stroke_weight(1)
				tp = self.tetherpos()
				line(tp.x, tp.y, tgt.pos.x, tgt.pos.y)

			if debug: #If debug then draw the current waypoint.
				v = Point(self.wpn.x * 16, self.wpn.y * 16)
				v.x += self.wp.x
				v.y += self.wp.y
				stroke(1,0,0,1)
				stroke_weight(2)
				line(self.wp.x, self.wp.y, v.x, v.y)
				stroke(1,1,1,1)
				stroke_weight(1)
				line(self.wp.x, self.wp.y, self.wp.x + 1, self.wp.y + 1)
				tint(1,1,0,1)

class killer(aimachine):
	###Hunter Killer AI machine.
	def __init__(self, scn):
		aimachine.__init__(self, scn, killermesh, 2)
		self.color = Color(1.00, 0.00, 1.00)
		self.shoot = sounds[2]
		self.downtime = killerdowntime
		self.state = self.down

	def reset(self, pos, angle):
		aimachine.reset(self, pos, angle)
		v = killervel * self.basevel()
		self.minvel = v
		self.maxvel = v
		self.firedelay = 0 #Reset the fire delay timer.
		self.state = self.hunt #Start hunding.
		#Set bullet speed and lifespan again just in case they have changed.
		for b in self.bullets:
			b.speed = aibulletspeed
			b.lifespan = aibulletlife

	def nextwaypoint(self):
		###Randomly create a new waypoint on screen.
		self.wp = Point(randint(0, self.scene.size.w), randint(0, self.scene.size.h))
		self.wpn = Point(self.pos.x - self.wp.x, self.pos.y - self.wp.y)
		normalize(self.wpn)

	def kill(self):
		self.downtime = killerdowntime #Reset the down time countdown timer.
		aimachine.kill(self)
		self.state = self.down

	def down(self, dt):
		###Down state, remain so until downtime is up.
		self.downtime -= dt
		if self.downtime <= 0:
			p, a = self.scene.startpos()
			self.reset(p, a)

	def checkfire(self, dt):
		#Check to see if we should fire.
		if self.firedelay > 0: #Wait until delay timer is up.
			self.firedelay = max(0, self.firedelay - dt)
			return

		for p in self.scene.pl: #Check each player to see if in front of killer.
			v = Point(p.pos.x - self.pos.x, p.pos.y - self.pos.y)
			a1, _ = anglefromvector(v)
			da = deltaangle(self.angle, a1)
			if abs(da) < 0.07: #If delta angle is within range shoot.
				self.firedelay = firedelay
				self.fire()

	def hunt(self, dt):
		###State to keep going to random waypoints and checking for fire opportunities.
		if self.checkdest():
			self.nextwaypoint()
		self.updatevels(dt)
		self.checkfire(dt)
		machine.update(self, dt)

	def update(self, dt): self.state(dt)

###Machine to represent a player.
class player(machine):

	def __init__(self, pos, scn, dir):
		machine.__init__(self, pos, playerfilter, scn, playermesh, numbullets)
		self.dir = dir #+ or - 1.
		self.startpos = Point(*pos)
		self.control = 0
		self.unstable = False
		self.reset()

	###Reset the player to original position.
	def reset(self):
		machine.reset(self)
		self.dead = 0
		self.pos.x = self.startpos.x
		self.pos.y = self.startpos.y
		self.vel.y = self.scale * 8 #Start out with a velocity to move onto screen.
		self.angle = -hpi * self.dir
		self.destangle = self.angle

	###Kill the player.
	def kill(self):
		mob.kill(self)
		self.dead = deadtime #Start dead timer.

	###Move the player.
	def move(self, dt):
		if self.control:
			da = deltaangle(self.angle, self.destangle)
			if da: #If delta angle adjust angular velocity.
				av = self.avel + da
				s = sgn(av)
				self.avel = min(pi, abs(av)) * s

	def update(self, dt):
		if self.on: #If on then update.
			self.move(dt)
			self.unstable = False
			b = Vector3(self.pos.x, self.pos.y, self.scale * .75)
			#Check if colliding with crate, if so add instability to turning.
			for m in self.scene.crates:
				if m.boundcheck(b):
					self.unstable = True
					break
			#Dampen angular velocity.
			self.avel = dampen(self.avel, self.brka * dt)
			#If not controlling linear velocity dampen that as well.
			if not self.control:
				self.slowdown(dt)

			machine.update(self, dt)
		else: #Death of player is different from killer which uses state functions
					# simply to show another way of doing it.  I prefer states.
			self.dead -= dt
			if self.dead <= 0: #As soon as dead time up reset.
				self.reset()

	###Calculate direction/velocity from movement button touch.
	def movetouch(self, touch):
		deltax = (touch.location.x - self.movepos.x)
		deltay = (touch.location.y - self.movepos.y)
		a, l = anglefromvector(Point(deltax, deltay))
		self.destangle = a
		if l > movesense:
			self.vel.y = l * movescale

	###Check left/right button pressed, return true if handled.
	def touch_began(self, touch):
		if self.on:
			tl = touch.location
			if tl in self.moverect: #If movement rectangle touched.
				self.movetouch(touch)
				self.control += 1
				return True
			if tl in self.shootrect: #If fire rectangle touched.
				self.fire()
				return True
		return False

	def touch_moved(self, touch):
		if self.on:
			tl = touch.location
			if tl in self.moverect: #If movement rectangle touched.
				self.movetouch(touch)
				return True

			tpl = touch.prev_location
			if tpl in self.moverect: #If previous location was in movement rectangle then stop movement.
				self.control = max(0, self.control - 1)
				return True

			if tl in self.shootrect: #If fire rectangle touched calculate anguler velocity.
			#NOTE: We don't check if previous location was in button, we just assume so.
				delta = touch.location.y - touch.prev_location.y
				av = delta * turnscale * self.dir
				if self.unstable and av: #If unstable (on crate) add random angular velocity.
					r = uniform(-uadj, uadj)
					self.angle = addangle(self.angle, r)
				self.avel += av
				return True
		return False

	###Touch ends.
	def touch_ended(self, touch):
		if self.on:
			tl = touch.location
			if tl in self.moverect: #If no longer touching movement button decrement control count.
				self.control = max(0, self.control - 1)
				return True
			return tl in self.shootrect #Return handled if intersects fire rectangle.
		return False

class MyScene(Scene):
	###Main scene.
	def setup(self):
		global screenrad
		# This will be called before the first frame is drawn.
		pos = self.bounds.center()
		cp = Point(*pos)
		pos.x = 0
		w = self.size.w
		h = self.size.h
		w3 = w / 5 #1/5th Screen width.
		w6 = w3 / 2 #1/10th Screen width.
		screenrad = hypot(w, h) * .5 #Set screen radius.
		self.pl = []
		plr = player(pos, self, 1.0) #Create player 1.
		self.pl.append(plr)
		plr.color = Color(1.00, 0.50, 0.00)
		plr.moverect = Rect(w - w3, 0, w3, w3) #Set movement button rectangle.
		plr.movepos = plr.moverect.center()
		plr.shootrect = Rect(w - w6, w3 * 2.25, w6, w3) #Set fire button rectangle.
		pos.x = w
		plr = player(pos, self, -1.0) #Create player 2.
		self.pl.append(plr)
		plr.color = Color(0.40, 1.00, 0.40)
		plr.shoot = sounds[1] #Change fire sound for player 2.
		plr.shootv = 0.3 #Set lower volume.
		plr.moverect = Rect(0, h - w3, w3, w3) #Set movement button rectangle.
		plr.movepos = plr.moverect.center()
		plr.shootrect = Rect(0, h - w3 * 2.25 - w3, w6, w3) #Set fire button rectangle.
		self.activebullets = [] #Array of active bullets.
		self.explosions = [] #Array of active explosions.
		self.controlalpha = 0.45 #Control rectangle alpha.
		self.wave = 0 #Wave counter.
		self.wpskipchance = wpskipchance
		self.killerinterval = killerinterval
		self.state = self.run
		self.gameovertxt = render_text('You\'ve been Ripped Off!', 'Copperplate', 32)
		self.pausetxt = render_text('Pause', 'Copperplate', 28)
		c = self.bounds.center()
		hh = self.pausetxt[1].w / 2
		self.pauserect = Rect(c.x - hh, 0, hh * 2, self.pausetxt[1].h)
		if mt:
			self.udstart = Event()
			self.uddone = Event()
			self.udthread = Thread(target=self.udthread)
			self.udthread.start()

		for s in sounds: load_effect(s) #pre-load sound effects.

		def makecrate(i):
		###Local function to create a crate mob.
			x = (int(i / 3) - 1) * cratespacing
			y = ((i % 3) - 1) * cratespacing
			cr = crate(Point(cp.x + x, cp.y + y), self)
			return cr

		self.crates = [makecrate(i) for i in xrange(numcrates)]
		self.robbers = [robber(self) for i in xrange(robbercount)]
		self.killers = [] #Start with 0 killers.
		self.numrobbers = 0

	###Remove crate from the crates array.
	def killcrate(self, cr): self.crates.remove(cr)

	def adjustdifficulty(self):
		###Adjust difficulty level based on # of waves.
		self.wpskipchance = wpskipchance + (self.wave * wpskipfactor)
		nk = min(self.wave / self.killerinterval, maxkillers)
		nk -= len(self.killers)
		while nk > 0: #Add killers.
			self.killerinterval += 2 #Adjust wave interval for next killer.
			nk -= 1
			k = killer(self)
			self.killers.append(k)

	def checkwave(self, dt):
		###Check to see if wave is complete.
		if not self.numrobbers: #If no more live robbers.
			if len(self.crates): #If still some live crates.
				self.wave += 1 #New wave.
				self.scoretxt = render_text('wave: ' + str(self.wave), 'Copperplate', 28)
				self.adjustdifficulty()
				self.startrobbers() #Restart all of the robbers.
			else:
				self.state = self.gameover

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
			for k in self.killers: #Check killers 1st.
				if checkcol(k):
					return True #If killer took hit exit.
			for r in self.robbers: #Check robbers, 1 bullet can hit many.
				hit |= checkcol(r)

		return hit

	def startpos(self):
		###Get a random start position just off screen.
		a = uniform(0, pi2) #Get angle from 0 to 2pi.
		p = Point(0, screenrad)
		rotpoint(a, p)
		c = self.bounds.center()
		p.x += c.x
		p.y += c.y
		return p, a

	def startrobbers(self):
		###Start all robbers.
		for r in self.robbers:
			if not r.on:
				c = choice(self.crates) #pick a target.
				p, a = self.startpos()
				r.reset(p, a, c)

	def udrobbers(self):
		###Update robbers and set # of live robbers.
		self.numrobbers = 0
		for r in self.robbers:
			self.numrobbers += r.update(self.dt)

	def udthread(self):
		###Mutli-threaded update.
		while True:
			self.udstart.wait() #Wait for main thread to signal update.
			self.udstart.clear() #Clear signal.
			self.udrobbers() #Update robbers.
			self.uddone.set() #Signal update done.

	def update(self, dt):
		###Update the scene.
		if debug:
			self.t0 = clock()
		if mt: self.udstart.set() #If multi-threaded signal update start.
		#if no screen touches reset control counters for safety (they can get out of sync).
		if len(self.touches) == 0:
			for p in self.pl:
				p.control = 0
		for p in self.pl: #Update players.
			p.update(dt)
		for k in self.killers: #Update killers.
			k.update(dt)
		#If not multi-threaded update robbers here.
		if not mt: self.udrobbers()
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
	def paused(self): pass

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
		self.checkwave(dt)
		self.update(dt)

	def drawcontrols(self):
		###Draw control boxes.
		if self.controlalpha:
			fill(0,0,0,0)
			stroke(0, 0, .5, self.controlalpha)
			stroke_weight(2)
			for p in self.pl:
				rect(*p.moverect)
			stroke(.5, 0, .5, self.controlalpha)
			for p in self.pl:
				rect(*p.shootrect)

	def drawscore(self):
		###Draw the score and pause text.
		tint(1,0,0)
		c = self.bounds.center()
		s = self.scoretxt[1]
		image(self.scoretxt[0], c.x - (s.w / 2), self.size.h - s.h, *s)
		clr = Color(1,1,0) if self.state == self.paused else Color(0.80, 0.40, 1)
		if debug: #In debug draw timing text.
			tmg = int((self.t1 - self.t0) * 1000.0)
			text(str(tmg), x=20, y=20, alignment=9)
		tint(*clr)
		s = self.pausetxt[1]
		image(self.pausetxt[0], c.x - (s.w / 2), 0, *s)

	def draw(self):
		###Draw all objects in the scene.
		background(0, 0, 0)
		self.state() #Update state.
		self.drawscore()
		self.drawcontrols()
		
		if mt and self.state == self.run: #Wait for other thread to finish.
			self.uddone.wait()
			self.uddone.clear()

		for cr in self.crates: cr.draw()
		for p in self.pl: p.draw()

		for k in self.killers: k.draw()
		for b in self.activebullets: b.draw()

		for r in self.robbers: r.draw()
		for e in self.explosions: e.draw()

	def checkpause(self, loc):
		###Check to see if pause button pressed.
		if loc in self.pauserect:
			play_effect(sounds[5])
			if self.state == self.paused:
				self.state = self.prevstate
			else:
				self.prevstate = self.state
				self.state = self.paused

	def touch_began(self, touch):
		###Handle touch events.
		for p in self.pl:
			if p.touch_began(touch):
				return

	def touch_moved(self, touch):
		###Handle touch move events.
		for p in self.pl:
			if p.touch_moved(touch):
				return

	def touch_ended(self, touch):
		###Handle touch end events.
		for p in self.pl:
			if p.touch_ended(touch):
				return
		self.checkpause(touch.location) #Check for pause button press.

run(MyScene(), LANDSCAPE)