#----------------------------------------------------------------------
# Copyright (c) 2012, Guy Carver
# All rights reserved.
# https://gist.github.com/GuyCarver/4116156
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
# FILE    monkey.py
# BY      Guy Carver
# DATE    11/19/2012 10:48 PM
#----------------------------------------------------------------------

from scene import *
from random import *
from sound import *
from math import sin

IPad = True
streeth = 44
divw = 32
sidewalkw = 64
sidewalkh = 44
numcars = 8
numfloaters = 10
offset = Point(0, 50)
waterspeed = Point(80, 25)
streetspeed = Point(100, 50)
badguyspeed = Point(2, 1)
cardelay = (0.25, 0.75, 0.025)
floatdelay = (1.0, 2.0, 0.025)
fontsize = 20 #Size of the font for display of score and tries..

models = [('Ambulance', 50), ('Bus', 64),('Car_1', 48), ('Car_2', 48),('Delivery_Truck', 64),
          ('Fire_Engine', 64), ('Police_Car', 50), ('Taxi', 50), ('Bus', 80), ('Railway_Car', 80)]

rivermodels = [('Sailboat', 64), ('Sailboat', 96), ('Sailboat', 160),
               ('Speedboat', 192), ('Speedboat', 96), ('Speedboat', 128),
               ('Whale', 64), ('Whale', 96), ('Whale', 192)]

def getrect(pos):
	###return a rect at given cell location with size of cell.
	return Rect(pos.x * divw + offset.x,
			 				pos.y * streeth + offset.y,
			 				divw, streeth)

	###-1 if < 0 otherwise 1
def sgn(val): return 1 if val >= 0 else -1

class badguy(object):
	###Object to represent the badguy running at the top of the screen.
	def __init__(self, y, scn):
		self.scene = scn
		w = divw
		self.right = scn.size.w - w
		x = uniform(w, self.right) #Pick random start position.
		self.dir = uniform(-w, w) #Pick random direction and speed.
		self.pos = Point(x, y)
		self.turntime = 3 #Time interval in seconds between decisions to turn around.
		self.timer = self.turntime
		self.setspeed()

	def setspeed(self): self.speed = uniform(1, 3)
	def changedir(self): self.dir = -self.dir

	def update(self, dt):
		###Update.
		self.pos.x -= self.dir * dt * self.speed
		if self.pos.x < 0:
			self.pos.x = 0
			self.changedir()
		elif self.pos.x > self.right:
			self.pos.x = self.right
			self.changedir()
		self.timer -= dt
		if self.timer <= 0: #If decision timer is up then randomly check to turn around.
			self.timer = self.turntime
			if random() < 0.2: #20% chance of turning around.
				self.changedir()

	def draw(self):
		###Draw the badguy.
		tint(1,1,1)
		x = self.pos.x
		if self.dir < 0:
			x -= self.dir
		r = Rect(x, self.pos.y, self.dir, streeth)
		image('Runner', *r)

	def collide(self, rect):
		###Check collision of runner with given rectangle.
		r = Rect(self.pos.x, self.pos.y, divw, streeth)
		return r.intersects(rect)

class target(object):
	###Object representing the target (family) at the top of the screen.

	###Set the position.
	def setpos(self, pos): self.frame = Rect(pos.x, pos.y, divw, streeth)

	def draw(self):
		###Draw the target.
		tint(1,1,1)
		image('Man_And_Woman', *self.frame)

	###Check collision with given rect.
	def collide(self, rct): return self.frame.intersects(rct)

class splash(object):
	###Water splash consists of a blue ripple and white splash.
	def __init__(self): self.on = False

	def set(self, pos):
		###Set the splash at the given position.
		d = divw / 2
		self.frame = Rect(pos.x + d, pos.y + d, 1, 1)
		self.on = True
		self.alpha = 0.8 #Ripple alpha.
		self.alpha2 = 1.0 #Splash alpha.
		set_volume(0.3)
		play_effect('Shot')

	def update(self, dt):
		###Update the splash.
		if self.on:
			d = divw * dt #Expand by divw/second.
			#Keep the center of the expanding splash at the same point.
			w = self.frame.w + d * 2 #Adjust the width by 2xd
			self.frame.x -= d #Subtrace d from x,y
			self.frame.y -= d
			self.frame.w = w #Set width/height to w.
			self.frame.h = w
			self.alpha = max(0.0, self.alpha - 1.5 * dt) #Adjust ripple alpha.
			self.alpha2 = max(0.0, self.alpha2 - 3 * dt) #Adjust splash alpha.
			self.on = self.alpha > 0 #Turn off when ripple alpha is 0.

	def draw(self):
		if self.on:
			a = min(1.0, self.alpha)
			tint(0,0,1,a)
			image('Red_Ring', *self.frame) #Draw blue ripple.
			tint(0.5,1,1,self.alpha2)
			image('Snowflake', *self.frame) #Draw white splash.

class splat(object):
	###Blood splat from getting run over.
	def __init__(self): self.on = False

	def set(self, pos):
		###Set the position of the splat.
		w = 24 if IPad else 12
		self.frame = Rect(pos.x, pos.y, w, w)
		self.on = True
		self.alpha = 2.0 #Alpha > 1 to keep it visible longer.
		set_volume(1)
		play_effect('Footstep' if randint(0, 1) else 'Jump')

	def update(self, dt):
		###Update splat.
		if self.on:
			self.alpha = max(0.0, self.alpha - 0.5 * dt) #Reduce alpha by .5/second.
			self.on = self.alpha > 0 #Turn off when alpha is 0.

	def draw(self):
		###If on draw the splat.
		if self.on:
			a = min(1.0, self.alpha) #Keep alpha between 0 and 1.
			tint(1,0,0, a) #Tint it red.
			image('Cloud', *self.frame)

class sidewalk(object):
	###Sidewalk object.
	def __init__(self, y, scn):
		x = scn.bounds.x
		w = scn.bounds.w
		self.frame = Rect(x, y, w, streeth)
		self.framesegment = Rect(x, y, sidewalkw, sidewalkh)
		self.count = int(w /sidewalkw) #Tile image for width of screen.
		self.image = 'PC_Ramp_South'

	###Set the image to draw on the sidewalk.
	def setimage(self, img): self.image = img

	###Update does nothing.
	def update(self, dt): pass

	def draw(self):
		###Draw the sidewalk.
		tint(1,1,1,1)
		p = Rect(*self.framesegment)
		p.y -= 24 if IPad else 12
		p.h += 50 if IPad else 25
		for i in range(self.count): #Loop for # of tiles.
			image(self.image, *p)
			p.x += sidewalkw #Adjust x to next tile position.

class car(object):
	###Object representing a car on the road.
	def __init__(self, pos, scn, left):
		self.start = 0 if left else scn.size.w #Start on left or right of screen.
		self.otherside = scn.size.w - self.start #Set destination to other side.
		self.scale_x = 1 if left else -1
		x = self.start + pos.x * self.scale_x
		self.frame = Rect(x, pos.y, 0, streeth)
		self.on = random() < 0.35 #Randomly turn the car on.
		self.setmodel()
		pos.x += abs(self.frame.w) * 2 * self.scale_x #Adjust position by 2 x width of our frame so next car isn't on top of us.
		self.prevx = x #Set previous x (in case we can ride the car).

	###Set vehicle speed in the direction indicated by scale_x.
	def setspeed(self, speed): self.vel = speed * self.scale_x

	def setmodel(self):
		###Randomly pick the model and set the frame size.
		div = -1 if IPad else -.5 #Negative because we go opposite direction of image.
		m = models[randint(0, len(models)-1)]
		self.image = m[0]
		self.frame.w = (m[1] * div) * self.scale_x
		self.end = self.otherside - self.frame.w

	###Check collision.
	def collide(self, rct): return self.on and self.frame.intersects(rct)

	def startpos(self):
		###Reset the start position.
		self.frame.x = self.start
		self.prevx = self.start

	def reset(self):
		###Reset the vehicle and turn on.
		self.setmodel()
		self.startpos()
		self.on = True

	def isfree(self):
		###Return true if the car is fully on screen indicating the
		### lane is free for another car to start.
		d = (self.frame.x + self.frame.w)
		if self.start: #if start is not 0 (left side) negate the point.
			d = -d
		return (self.start + d) > 0

	###Return the distance from last position to current position.
	### Used to move the player if "riding the vehicle".
	def deltax(self): return self.frame.x - self.prevx

	def update(self, dt):
		###Update the vehicle.
		if self.on:
			x = self.frame.x
			self.prevx = x
			x += self.vel * dt #Adjust x by velocity.
			self.frame.x = x
			#Set off if off end of screen.
			self.on = (x > self.end) if self.end < 0 else (x < self.end)

	def draw(self):
		###Draw the vehicle.
		if self.on:
			tint(1, 1, 1)
			image(self.image, *self.frame)

class floater(car):
	###Extend car to represent a vehicle on the water.

	def setmodel(self):
		###Set the model.
		div = -1 if IPad else -.5 #Negative because images are backwards.
		i = randint(0, len(rivermodels)-1)
		m = rivermodels[i]
		self.image = m[0]
		self.frame.w = m[1] * div * self.scale_x
		self.end = self.otherside - self.frame.w
		self.sink = i > 5 #If index > 5 then it's a sinking vehicle.
		if self.sink: #Pick random sinking phase.
			self.phase = random() * (self.otherside - self.start)

	###Return true if submerged. -2 <= sine <= 0 and submerged if < -1.9
	def submerged(self): return self.sink and self.sine < -1.9

	def update(self, dt):
		###Update the vehicle.
		car.update(self, dt)
		if self.sink: #If sinkable then adjust the sine wave.
			self.sine = sin((self.frame.x + self.phase) * 0.01) - 1.0

	def draw(self):
		###Draw the vehicle.
		if self.on:
			if self.sink: #If sinkable then adjust y by sine wabe.
				r = Rect(*self.frame)
				r.y += (r.h * 0.5) * self.sine #Since sine is -2 - 0 we divide h by 2.
				tint(1, 1, 1)
				image(self.image, *r)
			else:
				car.draw(self)

class player(Layer):
	###Player.
	def __init__(self, pos, scn) :
		Layer.__init__(self)
		self.image = 'Monkey'
		self.background = Color(0,0,0,0)
		self.tint = Color(1,1,1,1)
		self.setframe(pos)
		self.start = pos
		self.rotation = 0
		self.score = 0
		self.tries = 1
		self.scene = scn
		scn.add_layer(self)

	#Return a new Point object representing the position.
	def getpos(self): return Point(self.frame.x, self.frame.y)

	def setframe(self, pos) :
		###set position rect.
		self.frame = Rect(pos.x, pos.y, divw, divw)
		self.moving = False
		self.supported = None

	def sink(self):
		###The vehicle we were riding sank.
		self.scene.splash.set(self.getpos())
		self.tries += 1
		self.reset()

	def hit(self):
		###We were run over.
		self.tries += 1
		self.reset()

	def finished(self):
		###We reached the target.
		self.score += 1
		set_volume(0.4)
		play_effect('Pulley')
		self.reset()

	def reset(self):
		###Put back at the beginning.
		self.setframe(self.start)
		self.remove_all_animations()

	###Set movement done.
	def movedone(self): self.moving = False

	def update(self, dt):
		###Update the player.
		Layer.update(self, dt)
		###If supported by a vehicle.
		if self.supported:
			if self.supported.submerged(): #If the vehicle is submerged.
				self.sink()
			else:
				d = self.supported.deltax() #Get amound to move to say on supporting vehicle.
				self.frame.x += d
				#Keep on screen.
				self.frame.x = max(self.scene.bounds.left(), min(self.scene.bounds.right() - self.frame.w + 1, self.frame.x))

	def moveit(self, dir) :
		###if not moving then start movement anims in the given direction.
		if not self.moving :
			torect = Rect(*self.frame)
			torect.x += dir.x * divw
			torect.x = min(max(self.scene.min.x, torect.x), self.scene.max.x - divw)
			torect.y += dir.y * streeth
			torect.y = min(max(self.scene.min.y, torect.y), self.scene.max.y - streeth)
			self.moving = True
			set_volume(0.4)
			play_effect('Jump_5')
			crv = curve_ease_back_out #if dir.y else curve_linear
			#Animate frame and call movedone when finished.
			self.animate('frame', torect, 0.5, curve=crv, completion = self.movedone)

class stream(sidewalk):
	###Extend sidewalk object to represent a river stream.
	def __init__(self, y, scn, left):
		sidewalk.__init__(self, y, scn)
		pos = Point(scn.bounds.x, y)
		#Create the floaters.
		self.floaters = [floater(pos, scn, left) for i in xrange(numfloaters)]
		self.setspeed()
		self.lastfloater = None

	def setspeed(self):
		###Set random speed of the stream.
		self.speed = random() * waterspeed.x + waterspeed.y
		for f in self.floaters: #Adjust speed of floaters in this stream.
			f.setspeed(self.speed)

	def collide(self, rct):
		###Check collision on this stream and return stream, floater of collision.
		s = self.frame.intersects(rct)
		if s: #If colliding with the stream check the floaters.
			for f in self.floaters:
				if f.collide(rct):
					return (s, f) #Return stream, floater.
		return (s, None)

	def startfloater(self):
		###Start a floater.
		if self.lastfloater: #Make sure last floater is free 1st.
			if not self.lastfloater.isfree():
				return False

		for f in self.floaters:
			if not f.on: #Find a floater that is off.
				f.reset() #Start floater.
				self.lastfloater = f
				break
		return True

	def update(self, dt):
		###Update floaters in the stream.
		for f in self.floaters:
			f.update(dt)

	def draw(self):
		###Draw sidewalk and it's floaters.
		sidewalk.draw(self)
		for f in self.floaters:
			f.draw()

class street(object):
	###Object to represent a lane on the street.
	def __init__(self, y, scn, left):
		x = scn.bounds.x
		w = scn.bounds.w
		self.left = left
		self.lastcar = None
		self.frame = Rect(x, y, w, streeth)
		self.divider = Rect(x, self.frame.top() - 2, w, 2)
		if left:
			self.count = int(w / divw)
			self.divider.w = divw - 4 #Leave 4 pixels between tiles to make dash.
		else:
			self.count = 1 #Solid line.
		pos = Point(x, y)
		#Add cars, pos will be adjusted by the car constructor.
		self.cars = [car(pos, scn, left) for i in xrange(numcars)]
		self.setspeed()

	def setspeed(self):
		###Set speed to random range and adjust lane speed.
		self.speed = random() * streetspeed.x + streetspeed.y
		for c in self.cars:
			c.setspeed(self.speed)

	def collide(self, rct):
		###Check collision of lane and cars in lane.  Return true if collide.
		if self.frame.intersects(rct):
			for c in self.cars:
				if c.collide(rct):
					return True
		return False

	def startcar(self):
		###Start a car.
		if self.lastcar:
			if not self.lastcar.isfree(): #Wait til last car is on screen.
				return False
		#Find a free car and start it.
		for c in self.cars:
			if not c.on:
				c.reset()
				self.lastcar = c
				break
		return True

	def update(self, dt):
		###Update cars in lane.
		for c in self.cars:
			c.update(dt)

	def draw(self):
		###Draw lane.
		fill(0.40, 0.40, 0.40)
		rect(*self.frame)
		fill(1.00, 1.00, 0.00)
		p = Rect(*self.divider)
		for i in xrange(self.count):
			rect(*p)
			p.x += divw

	def drawcars(self):
		###Draw cars in lane.
		for c in self.cars:
			c.draw()

class MyScene(Scene):
	###Scene.
	def setup(self):
		# This will be called before the first frame is drawn.
		global IPad
		global streeth
		global divw
		global sidewalkw
		global sidewalkh
		global offset
		IPad = self.size.w > 700
		if not IPad: #On IPhone all of these values are half.
			streetspeed.x /= 2
			streetspeed.y /= 2
			waterspeed.x /= 2
			waterspeed.y /= 2
			badguyspeed.x /= 2
			badguyspeed.y /= 2
			streeth /= 2
			divw /= 2
			sidewalkw /= 2
			sidewalkh /= 2
			offset.y /= 2
		self.root_layer = Layer(self.bounds)
		self.org = Rect(self.bounds.x + 8, self.bounds.y + 8, self.bounds.w - 16, self.bounds.h - 16)
		self.splat = splat()
		self.splash = splash()
		pos = Point(*offset)
		self.min = Point(*pos)
		self.start = sidewalk(pos.y, self)
		px = divw * 16 #Middle tile.
		self.player = player(Point(px, pos.y), self)
		pos.y += streeth

		def makelane(i):
			###Local function to create a lane.
			l = street(pos.y, self, (i & 1) == 0)
			pos.y += streeth #Adjust y by lane height.
			return l

		def makestream(i):
			###Local function to create a stream.
			s = stream(pos.y, self, (i & 1))
			s.setimage('PC_Water_Block')
			pos.y += streeth #Adjust y by stream height.
			return s

		self.lanes = [makelane(i) for i in xrange(6)]
		self.middle = sidewalk(pos.y, self)
		pos.y += streeth
		self.middle.setimage('PC_Grass_Block')
		self.streams = [makestream(i) for i in xrange(6)]
		self.streams.reverse()
		self.end = sidewalk(pos.y, self)
		self.badguy = badguy(pos.y, self)
		self.target = target()
		pos.y += streeth
		pos.x = self.bounds.w
		self.max = Point(*pos)
		pos.y += 5 #Score is up 5 pixels.
		pos.x = self.bounds.left()
		self.scorepos = Point(*pos)
		pos.x = self.bounds.right() - 100 #Tries are in 100 pixels from right.
		self.trypos = Point(*pos)
		self.reset()

	###Return false.
	def should_rotate(self, rot): return False

	def settarget(self):
		###Set target to random position on sidewalk at top of screen.
		self.target.setpos(Point(random() * (self.size.w - sidewalkw * 2) + sidewalkw, self.end.frame.y))

	def reset(self):
		###Reset the game.
		self.finished = False
		self.cardelay = cardelay[1]
		self.floatdelay = floatdelay[0]
		self.startcar()
		self.startfloater()
		self.settarget()

	def newvelocities(self):
		###Set new velicities for street and streams.
		for s in self.streams:
			s.setspeed()
		for l in self.lanes:
			l.setspeed()
		self.badguy.setspeed()

	def startfloater(self):
		###Start a random floater.
		inds = range(0, len(self.streams))
		shuffle(inds)
		for i in inds: #Try each stream until a floater started.
			if self.streams[i].startfloater():
				break
		#Restart the delay timer.
		self.delay(self.floatdelay, self.startfloater)

	def startcar(self):
		###Start a random car.
		inds = range(0, len(self.lanes))
		shuffle(inds)
		for i in inds: #Try each lane until a car is started.
			if self.lanes[i].startcar():
				break
		#Restart the delay timer.
		self.delay(self.cardelay, self.startcar)

	def movedir(self, pos):
		###calculate movement direction.
		pos.x -= self.tstart.x
		pos.y -= self.tstart.y
		ax = abs(pos.x)
		ay = abs(pos.y)
		if ax > ay :
			return Point(sgn(pos.x), 0)

		return Point(0, sgn(pos.y))

	def success(self):
		###Player reached target.
		self.player.finished()
		self.newvelocities()
		self.settarget()
		self.cardelay = max(cardelay[0], self.cardelay - cardelay[2])
		self.floatdelay = min(floatdelay[1], self.floatdelay + floatdelay[2])

	def update(self):
		###Update scene.
		rct = Rect(*self.player.frame)
		rct.x += 8 #Adjust player rectangle used for collision detection.
		rct.w -= 16
		rct.y += 8
		rct.h -= 16
		b = False
		#Update cars.
		for l in self.lanes:
			l.update(self.dt)
		#Update streams.
		for s in self.streams:
			s.update(self.dt)
		#Check collision with cars.
		for l in self.lanes:
			if l.collide(rct): #If collision draw splat and reset player.
				b = True
				self.splat.set(self.player.getpos())
				self.player.hit()
				break
		#If no collision check streams.
		if not self.player.moving: #Only check support if not jumping.
			if not b:
				self.player.supported = None #Clear support.
				#Check floaters in streams for support.
				for s in self.streams:
					b, cl = s.collide(rct)
					if b: #If on a stream.
						if cl: #If a support object.
							self.player.supported = cl
						else: #No support so we sink.
							self.player.sink()
						break

			#If didn't collide.
			if not b:
				if self.target.collide(rct):
					self.success() #At target.
				elif self.badguy.collide(rct):
					self.player.hit() #Caught by badguy.

		self.badguy.update(self.dt)
		self.splat.update(self.dt)
		self.splash.update(self.dt)

	def drawscore(self):
		###Draw the score strings.
		tint(1,1,0,1)
		text('score: ' + str(self.player.score), 'Copperplate-Bold', fontsize, *self.scorepos.as_tuple(), alignment=9)
		text('tries: ' + str(self.player.tries), 'Copperplate-Bold', fontsize, *self.trypos.as_tuple(), alignment=7)

	def draw(self):
		# This will be called for every frame (typically 60 times per second).
		self.root_layer.update(self.dt)
		self.update()
		background(0,0,0)

		self.end.draw()

		for l in self.streams: l.draw()
		self.middle.draw()
		for l in self.lanes: l.draw()

		self.splash.draw()
		self.badguy.draw()
		self.target.draw()

		self.splat.draw()
		#Draw cars after splat
		for l in self.lanes: l.drawcars()

		self.start.draw()
		self.root_layer.draw()
		self.drawscore()

	###Handle touch begin event.
	def touch_began(self, touch): self.tstart = touch.location

	def touch_ended(self, touch):
		#Handle touch end event.
		if self.finished :
			self.reset()
		else: #Calculate swipe direction and move player.
			d = self.movedir(touch.location)
			self.player.moveit(d)

run(MyScene(), LANDSCAPE)