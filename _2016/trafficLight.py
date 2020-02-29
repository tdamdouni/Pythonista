from __future__ import print_function
# https://gist.github.com/TutorialDoctor/1e65fbe19e5a3acbb3d3

# Traffic Light
# By the Tutorial Doctor

# THE CLASS
#--------------------------------------------------
class TrafficLight():
	GREEN = [1,0,0]
	YELLOW = [0,1,0]
	RED = [0,0,1]
	
	def __init__(self):
		self.state = [0,0,0]
	
	def signal(self):
		if self.state==TrafficLight.RED:
			return 'stop'
		elif self.state==TrafficLight.GREEN:
			return 'go'
		elif self.state==TrafficLight.YELLOW:
			return 'slow down'
	
	def switchIndex(self):
		for switch in self.state:
			if switch==1:
				return self.state.index(switch)

	def __str__(self):
		return self.signal()
#--------------------------------------------------


# IMPLEMENTATION
#--------------------------------------------------
light = TrafficLight()
print(light.state)
light.state=TrafficLight.RED
print(light.signal())
print(light.switchIndex())
print(help(light))
#--------------------------------------------------
