# https://gist.github.com/anonymous/7f46b31bd43959f937b58a54a24e91a0

from objc_util import *
from ctypes import *
from scene import *

load_framework('Foundation')
load_framework('GameplayKit')

GKEntity = ObjCClass('GKEntity')
GKAgent2D = ObjCClass('GKAgent2D')
GKBehavior = ObjCClass('GKBehavior')
GKGoal = ObjCClass('GKGoal')

class float2(Structure):
	_fields_ = [('x',c_float),('y',c_float)]
	
def agentWillUpdate_(_self,_cmd,agent):
	a = ObjCInstance(agent)
	pos = a.position(argtypes=[],restype=float2)
	
def agentDidUpdate_(_self,_cmd,agent):
	a = ObjCInstance(agent)
	pos = a.position(argtypes=[],restype=float2)
	
	print('New y' + ': ' + str(pos.y))
	
delegate = create_objc_class('AgentDelegate',NSObject,methods=[agentWillUpdate_,agentDidUpdate_],protocols=['GKAgentDelegate'])
	
agent = GKAgent2D.alloc().init()
agent.mass = 0.1
agent.maxSpeed = 50
agent.maxAcceleration = 1000
agent.behavior = GKBehavior.behaviorWithGoal_weight_(GKGoal.goalToWander_(4), 1.0)
agent.delegate = delegate.alloc().init()

# Create new float2
n = float2()
n.x = 20
n.y = 20

# Set new float2 to GKAgent2D instance
agent.setPosition_(n,argtypes=[float2],restype=None)
# Get position from GKAgent2D instance
pos = agent.position(argtypes=[],restype=float2)
# x is properly set
print(pos.x)
# ERROR: y is still 0
print(pos.y)

class TestScene(Scene):
	def setup(self):
		print('Loaded')
		
	def update(self):
		agent.updateWithDeltaTime_(self.dt)

# Uncomment if you want to test GKAgentDelegate
#run(TestScene())
