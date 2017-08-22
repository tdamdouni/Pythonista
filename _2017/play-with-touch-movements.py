# https://forum.omz-software.com/topic/4143/how-do-i-do-to-play-the-movements-registered-in-the-scene/7

import scene,ui

class MyScene(scene.Scene):
	def __init__(self, in_dot_color=scene.Color(0, 0, 0, 1)):
		super().__init__()
		self.dot_color = in_dot_color
		self.touch = None
		self.points=[]
		self.timing=[]
		
	def draw(self):
		''' real time drawing only'''
		scene.background(0, 0, 0)
		if self.touch:
			scene.fill(self.spot_color)
			loc = self.touch.location
			scene.ellipse(loc.x - 50, loc.y - 50, 100, 100)
			scene.text('{}, {}'.format(*loc), 'Futura', 20, 100, 50)
			
	def touch_began(self, touch):
		'''register initial point and time'''
		self.points=[touch]
		self.timing=[0]
		self.touch = touch
		self.t0=self.t
		loc=touch.location
		self.spot_color=(loc.x/self.bounds.width, loc.y/self.bounds.height, .5)
		
	def touch_moved(self, touch):
		'''Record points and relative timing '''
		self.touch = touch
		self.points.append(touch)
		self.timing.append(self.t-self.t0)
	def touch_ended(self, touch):
		'''instantiate a shapenode, and animate it'''
		self.touch = None
		self.spot=scene.ShapeNode(path=ui.Path.oval(0,0,100,100),parent=self)
		self.spot.fill_color=self.spot_color
		self.spot.position=self.points[0].location
		actions=[]
		for i in range(len(self.points)-1):
			duration=self.timing[i+1]-self.timing[i]
			loc=self.points[i].location
			actions.append(scene.Action.move_to(*loc,duration))
			self.spot.run_action(scene.Action.repeat_forever(scene.Action.sequence(actions)))
			
s=MyScene()
scene.run(s, show_fps=True)

