# coding: utf-8

# https://gist.github.com/offe/48c833fc5bfad3571bb1

# https://forum.omz-software.com/topic/2393/beta-boids-with-a-crash

from __future__ import print_function
from scene import *
import random
import math
from colorsys import hsv_to_rgb

import time
import pickle

BOID_SIZE = 36
RANGE = 4 * BOID_SIZE
MAX_SPEED = 200
MAX_ACCELERATION = 200
MAX_FORCE = 0.05
OBSTACLE_SIZE = 3*BOID_SIZE

def random_within_bounds(bounds):
	return Point(random.uniform(bounds.min_x, bounds.max_x), 
							 random.uniform(bounds.min_y, bounds.max_y))

def vector_length(v):
	return math.sqrt(v.x*v.x + v.y*v.y)
	
def vector_normalize(v):
	d = vector_length(v)
	if d > 0.001:
		v /= d
	return v
	
def random_normalized():
	a = random.random() * 2 * math.pi
	return Point(math.sin(a), math.cos(a))
	
def vector_clamp(v, min_length, max_length):
	d = vector_length(v)
	if d > max_length:
		v *= max_length / d
	elif d < min_length:
		v *= min_length / d
	return v

def boid_can_see(boid, e):
	if e is boid:
		return False
	center_of_view = boid.position + vector_normalize(boid.vel) * RANGE / 2
	return vector_length(e.position - center_of_view) <= RANGE

def torus_diff_vector(a, b, (w, h)):
	d = a - b
	d = Point((d.x + 3*w/2) % w - w/2, (d.y + 3*h/2) % h - h/2)
	return d

class MyScene (Scene):
	def setup(self):
		self.read_crash_times()
		self.disperse = False
		self.background_color = 'black'
		
		self.obstacles = [SpriteNode('iow:record_256', 
																 position=random_within_bounds(self.bounds), 
																 size=(OBSTACLE_SIZE, OBSTACLE_SIZE), 
																 color='#444',
																 parent=self) 
									for _ in xrange(10)]
		
		self.boids = [self.new_boid() for _ in xrange(12)]
		for boid in self.boids:
			#boid.friends = random.sample(self.boids, 5)
			boid.friends = self.boids
		self.t = 0
	
	def new_boid(self):
		boid = SpriteNode('iow:ios7_paperplane_256', 
											 position=random_within_bounds(self.bounds), 
											 size=(BOID_SIZE, BOID_SIZE), 
											 parent=self) 
		boid.vel = random.uniform(0, MAX_SPEED)*random_normalized()
		boid.color = hsv_to_rgb((random.random()+1)/3, 0.9, 1.0)
		return boid
	
	def did_change_size(self):
		pass
	
	def cohesion(self, boid, seen):
		v = sum((n.position for n in seen), Point(0,0))
		return v / len(seen) - boid.position
	
	def separation(self, boid, seen):
		f = Point(0, 0)
		for neighbour in seen:
			v = neighbour.position - boid.position
			d = vector_length(v)
			if d < BOID_SIZE:
				f -= vector_normalize(v) * (BOID_SIZE-d)
		return f
		
	def alignment(self, boid, seen):
		v = sum((n.vel for n in seen), Point(0,0))
		return v / len(seen) - boid.vel
	
	def obstacle_separation(self, boid):
		f = Point(0, 0)
		for obstacle in self.obstacles:
			v = torus_diff_vector(obstacle.position, boid.position, self.size)
			d = vector_length(v)
			min_dist = BOID_SIZE + OBSTACLE_SIZE
			if d < min_dist:
				power = (min_dist - d) ** 2
				f -= vector_normalize(v) * power # away
				#heading = vector_normalize(boid.vel) # Wanted to turn full left or right to avoid. does not work
				#dot = (boid.vel.x*v.x + boid.vel.y*v.y)
				#f += math.copysign(1.0, dot) * (Point(-heading.y, heading.x) * power)
		return f
	
	def update_steering(self):
		for boid in self.boids:
			v = 100*self.obstacle_separation(boid)
			v += 0.2*random_normalized()
			seen = [n for n in boid.friends if boid_can_see(boid, n)]
			if seen:
				v += 0.2*self.cohesion(boid, seen) * (-1 if self.disperse else 1)
				v += 1*self.separation(boid, seen)
				v += 0.3*self.alignment(boid, seen) * (-1 if self.disperse else 1)
			boid.acc = vector_normalize(v) * MAX_ACCELERATION
			
	def update_positions(self):
		for boid in self.boids:
			boid.vel += boid.acc * self.dt
			boid.vel = vector_clamp(boid.vel, MAX_SPEED*.5, MAX_SPEED)
			boid.position += boid.vel * self.dt
			boid.rotation = math.atan2(boid.vel.y, boid.vel.x) - math.pi / 4 # Paper plane is at 45 degrees
			
			# Torus wrap
			x, y = boid.position
			w, h = self.size
			boid.position = Point(x % w, y % h)
	
	def update(self):
		self.t += self.dt
		self.write_crash_times()
		#print self.t
		self.update_steering()
		self.update_positions()
	
	def stop(self):
		self.end_crash_times()
	
	def touch_began(self, touch):
		self.disperse = True
	
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		self.disperse = False
		
	def crash_file_name(self):
		return 'crashtimes'
		
	def read_crash_times(self):
		try:
			with open(self.crash_file_name()) as f:
				times = pickle.load(f)
		except IOError as e:
			print(e)
			times = []
		self.crash_times = times
		print(self.crash_times)
		print()
		self.start_time = time.time()
		self.crash_times.append(0.0)

	def write_crash_times(self):
		# update() gets called a few times after stop() is called
		if self.start_time is None:
			return
		self.crash_times[-1] = time.time() - self.start_time
		with open(self.crash_file_name(), 'wb') as f:
			pickle.dump(self.crash_times, f)

	def end_crash_times(self):
		del self.crash_times[-1]
		with open('crashtimes', 'wb') as f:
			pickle.dump(self.crash_times, f)
		self.start_time = None

if __name__ == '__main__':
	run(MyScene(), show_fps=True)