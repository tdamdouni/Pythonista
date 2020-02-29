from __future__ import print_function
# https://forum.omz-software.com/topic/3165/scene-action-nodes-class-and-sprite-dynamic-access

# Sample code issue : how to access dynamically to a sprite Bbox in a Node playing an action

from scene import *
A = Action

class MyNode (Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		
		self.MySprite = SpriteNode(color = 'red', size = (32,32), parent = self)
		
	def SpriteBbox (self, Scene):
		return Rect(self.MySprite.position.x-(self.MySprite.size.x)/2,self.MySprite.position.y -(self.MySprite.size.y)/2,self.MySprite.size.x,self.MySprite.size.y)
		
class MyScene (Scene):
	def setup(self):
		self.background_color='#ffffff'
	#Instance in Scene
		self.MyObject = MyNode(position = self.size/2, parent = self)
	#Action
		self.MyAction = A.sequence(A.move_by(-150,-150,2),A.move_by(150,150,2))
		self.MyObject.run_action(A.repeat(self.MyAction,-1))
		pass
		
	def update(self):
		# Direct access using Scene : Not working, returns original Bbox, not updated
		print(self.MyObject.MySprite.bbox)
		print(self.MyObject.bbox)
		
		#Same result using a Method in the Class
		print(self.MyObject.SpriteBbox(Scene))
		print(self.MyObject.bbox)
		pass
		
if __name__ == '__main__':
	run(MyScene(), show_fps=False)
	
# Hi, you should call bbox on MyObject, not on MySprite. So the line should be:

# print self.MyObject.bbox

# The reason is that the node you added to the scene as MyObject is an instance of MyNode. The MySprite node you set inside the init of MyNode has self as a parent, which means an instance of MyNode. This also means that the bbox of MySprite will be measured in the coordinate system of it's parent (the instance of MyNode) and will thus be constant in this case because MySprite is not moving: the instance of MyNode is moving.

