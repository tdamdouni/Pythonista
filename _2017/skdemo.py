# https://gist.github.com/anonymous/2530353b2a41c19746bf9c0e0fa9a57f

# https://forum.omz-software.com/topic/4254/spritekit-contactdelegate-doesn-t-work

# https://github.com/jbking/pythonista-misc/blob/master/spritekit/skview-demo.py

import random
import ui
from objc_util import *

load_framework('SpriteKit')

SKView = ObjCClass('SKView')
SKScene = ObjCClass('SKScene')
SKShapeNode = ObjCClass('SKShapeNode')
SKPhysicsBody = ObjCClass('SKPhysicsBody')

def create_circle_shape(point):
	radius = random.randint(25, 45)
	node = SKShapeNode.shapeNodeWithCircleOfRadius_(radius)
	node.position = point
	node.physicsBody = SKPhysicsBody.bodyWithCircleOfRadius_(radius)
	return node


def create_box_shape(point):
	width = random.randint(42, 80)
	height = random.randint(42, 80)
	size = CGSize(width, height)
	node = SKShapeNode.shapeNodeWithRectOfSize_(size)
	node.position = point
	node.physicsBody = SKPhysicsBody.bodyWithRectangleOfSize_(size)
	return node


def update_(_self, _cmd, current_time):
	scene = ObjCInstance(_self)
	for child in scene.children():
		if child.position().y < 0:
			child.removeFromParent()

def random_color():
	return UIColor.color(red=random.random(), green=random.random(), blue=random.random(), alpha=1.0)


def touchesBegan_withEvent_(_self, _cmd, _touches, event):
	scene = ObjCInstance(_self)
	scene.physicsBody = SKPhysicsBody.bodyWithEdgeLoopFromRect_(CGRect(CGPoint(0,0),CGSize(300,300)))
	touches = ObjCInstance(_touches)
	for id, touch in enumerate(touches):
		point = touch.locationInNode_(scene)
		node = random.choice([
		create_circle_shape,
		create_box_shape
		])(point)
		node.fillColor = random_color()
		scene.addChild_(node)

def didBeginContact_(_self,_cmd,contact):
	print("Contacting")

DemoScene = create_objc_class(
'DemoScene',
SKScene,
methods=[
update_,
touchesBegan_withEvent_,
didBeginContact_
],
protocols=['SKPhysicsContactDelegate'])

class DemoView(ui.View):

	def __init__(self):
		screen_size = ui.get_screen_size()
		rect = CGRect(CGPoint(0, 0),CGSize(screen_size.w, screen_size.h))
		skview = SKView.alloc().initWithFrame_(rect)
		
		ObjCInstance(self).addSubview(skview)
		self.skview = skview
		scene = DemoScene.sceneWithSize_(rect.size)
		scene.physicsWorld().setContactDelegate_(scene)
		print(scene.physicsWorld().contactDelegate())
		scene.backgroundColor = UIColor.color(red=0.2, green=0.5, blue=0.2, alpha=1.0)
		skview.presentScene_(scene)
		self.scene = scene


if __name__ == '__main__':
	view = DemoView()
	view.present(hide_title_bar=False)
