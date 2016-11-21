# coding: utf-8

# http://youtu.be/fXXmeP9TvBg

import scene
import ui

"""
Carwash example.

Covers:

- Waiting for other processes
- Resources: Resource

Scenario:
  A carwash has a limited number of washing machines and defines
  a washing processes that takes some (random) time.

  Car processes arrive at the carwash at a random time. If one washing
  machine is available, they start the washing process and wait for it
  to finish. If not, they wait until they an use one.

"""
import random

import simpy

event_list = []


RANDOM_SEED = 42
NUM_MACHINES = 3  # Number of machines in the carwash
WASHTIME = 10     # Minutes it takes to clean a car
T_INTER = 7       # Create a car every ~7 minutes
SIM_TIME = 100     # Simulation time in minutes


class Carwash(object):
	"""A carwash has a limited number of machines (``NUM_MACHINES``) to
	clean cars in parallel.
	
	Cars have to request one of the machines. When they got one, they
	can start the washing processes and wait for it to finish (which
	takes ``washtime`` minutes).
	
	"""
	def __init__(self, env, num_machines, washtime):
		self.env = env
		self.machine = simpy.Resource(env, num_machines)
		self.washtime = washtime
		
	def wash(self, car):
		"""The washing processes. It takes a ``car`` processes and tries
		to clean it."""
		yield self.env.timeout(WASHTIME)
		percent = random.randint(50, 99)
		event_list.append((env.now, 'carwash removed', percent, car))
		print("Carwash removed %d%% of %s's dirt." %
		(percent, car))
		
		
def car(env, name, cw):
	"""The car process (each car has a ``name``) arrives at the carwash
	(``cw``) and requests a cleaning machine.
	
	It then starts the washing process, waits for it to finish and
	leaves to never come back ...
	
	"""
	event_list.append((env.now, 'arrives', name))
	print('%s arrives at the carwash at %.2f.' % (name, env.now))
	with cw.machine.request() as request:
		#print(dir(request.resource.users)) #, repr(request.resource.request))
		cnt = request.resource.count
		yield request
		#print(request.resource.capacity, request.resource.count)
		print('%s enters the carwash at %.2f.' % (name, env.now))
		event_list.append((env.now, 'enters', name, cnt))
		yield env.process(cw.wash(name))
		
		print('%s leaves the carwash at %.2f.' % (name, env.now))
		event_list.append((env.now,'leaves', name, cnt))
		
		
def setup(env, num_machines, washtime, t_inter):
	"""Create a carwash, a number of initial cars and keep creating cars
	approx. every ``t_inter`` minutes."""
	# Create the carwash
	carwash = Carwash(env, num_machines, washtime)
	
	# Create 4 initial cars
	for i in range(4):
		env.process(car(env, 'Car %d' % i, carwash))
		
	# Create more cars while the simulation is running
	while True:
		yield env.timeout(random.randint(t_inter-2, t_inter+2))
		i += 1
		env.process(car(env, 'Car %d' % i, carwash))
		
class MyScene (scene.Scene):
	def setup(self):
		self.leaveq = scene.LabelNode('',
		anchor_point=(1.0, .5),
		position=(self.size[0]/2-100, self.size[1]/2),
		parent=self)
		self.washq  = scene.LabelNode('',
		anchor_point=(1.0,.5),
		position=(self.size[0]/2, self.size[1]/2),
		parent=self)
		self.frontq = scene.LabelNode('',
		anchor_point=(0, .5),
		position=(self.size[0]/2+100, self.size[1]/2),
		parent=self)
		self.time_count_checkpoint = 0
		self.time_count = 0
		self.time_interval = 20
		self.update_event_list()
		
	def update_event_list(self):
		global event_list
		if env.peek() >= 10000:
			return
		event_list = []
		self.time_count_checkpoint += self.time_interval
		while env.peek() < (self.time_count_checkpoint):
			env.step()
		self.event_dict = {}
		for e in event_list:
			if e[0] in self.event_dict:
				self.event_dict[int(e[0])].append(e[1:])
			else:
				self.event_dict[int(e[0])] = [e[1:]]
				
	def process(self, time_count, e):
		event_type = e[0]
		#🚕  🚗
		if event_type == 'arrives':
			self.frontq.text  = '🚗' + self.frontq.text
		elif event_type == 'carwash removed':
			self.frontq.text = self.frontq.text[:-1]
		elif event_type == 'enters':
			self.washq.text += '🚗'
		elif event_type == 'leaves':
			self.washq.text = self.washq.text[:-1]
			self.leaveq.text = '🚗' + self.leaveq.text
			if len(self.leaveq.text) > 16:
				self.leaveq.text = ''
				
	def update(self):
		if self.time_count >= (self.time_count_checkpoint):
			self.update_event_list()
		if self.time_count in self.event_dict:
			for e in self.event_dict[self.time_count]:
				self.process(self.time_count, e)
		self.time_count += 1
		
# Setup and start the simulation
print('Carwash')
print('Check out http://youtu.be/fXXmeP9TvBg while simulating ... ;-)')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_MACHINES, WASHTIME, T_INTER))

# Execute!
#env.run(until=SIM_TIME)
scene.run(MyScene(), frame_interval=10, show_fps=True)

