# coding: utf-8

# https://forum.omz-software.com/topic/2801/spritekit/5

# some code to test out SpriteKit and its physics engine
# tried to generalize the functionality into utility
# functions and will be looking at a better way

from objc_util import *
import ui
import random


UIViewController = ObjCClass('UIViewController')
UIBarButtonItem = ObjCClass('UIBarButtonItem')
UIColor = ObjCClass('UIColor')
UIScreen = ObjCClass('UIScreen')
UIImage = ObjCClass('UIImage')
SKView = ObjCClass('SKView')
SKScene = ObjCClass('SKScene')
SKLabelNode = ObjCClass('SKLabelNode')
SKPhysicsBody = ObjCClass('SKPhysicsBody')
SKSpriteNode = ObjCClass('SKSpriteNode')
SKShapeNode = ObjCClass('SKShapeNode')
SKTexture = ObjCClass('SKTexture')

# should refactor in class and/or actual module
skview = None

# utility functions to generate physics based sprite or
# shape nodes of random sizes

def addCircleShape(target_scene, x, y):
	radius = random.randint(25,45)
	node = SKShapeNode.shapeNodeWithCircleOfRadius_(radius)
	node.position = CGPoint(x, y)
	body = SKPhysicsBody.bodyWithCircleOfRadius_(radius)
	node.physicsBody = body
	target_scene.addChild_(node)
	
def addBoxShape(target_scene, x, y):
	width = random.randint(42,80)
	height = random.randint(42,80)
	size = CGSize(width,height)
	node = SKShapeNode.shapeNodeWithRectOfSize_(size)
	node.position = CGPoint(x, y)
	node.zRotation = random.random()
	body = SKPhysicsBody.bodyWithRectangleOfSize_(size)
	node.physicsBody = body
	target_scene.addChild_(node)
	
	
# This will create a texure and create a physics polygon
# from the transparent places; pass in alpha
# to include semi-transparent places
def addSpriteWithTexture(target_scene, texture, x, y, scale = True, keep_aspect=True, alpha = 0):
	img = ui.Image.named(texture)
	img_sz = img.size
	width = img_sz[0]
	height = img_sz[1]
	if scale:
		width = random.randint(42,80)
		if keep_aspect:
			ratio = width / img_sz[0]
			height = height * ratio
		else:
			height = random.randint(42,80)
	tex = SKTexture.textureWithImage_(img)
	size = CGSize(width,height)
	node = SKSpriteNode.spriteNodeWithTexture_(tex)
	node.size = size
	node.position = CGPoint(x, y)
	node.zRotation = random.random()
	if alpha == 0:
		body = SKPhysicsBody.bodyWithTexture_size_(tex, size)
		node.physicsBody = body
	else:
		body = SKPhysicsBody.bodyWithTexture_alphaThreshold_size_(tex, alpha, size)
		node.physicsBody = body
	target_scene.addChild_(node)
	
# was thinking this would be faster for physics but my
# simple tests didn't show much difference
def addSpriteWithRoundTexture(target_scene, texture, x, y):
	img = ui.Image.named(texture)
	tex = SKTexture.textureWithImage_(img)
	width = random.randint(42,80)
	height = width
	radius = width /2
	size = CGSize(width,height)
	node = SKSpriteNode.spriteNodeWithTexture_(tex)
	node.size = size
	node.position = CGPoint(x, y)
	node.zRotation = random.random()
	body = SKPhysicsBody.bodyWithCircleOfRadius_(radius)
	node.physicsBody = body
	target_scene.addChild_(node)
	
# the boundaries to keep the shapes in
def addBorder(target_scene, x,y,w,h):
	size = CGSize(w,h)
	node = SKShapeNode.shapeNodeWithRectOfSize_(size)
	node.position = CGPoint(x,y)
	node.lineWidth = 2
	node.fillColor = UIColor.blueColor()
	
	body = SKPhysicsBody.bodyWithRectangleOfSize_(size)
	body.dynamic = False
	node.physicsBody = body
	target_scene.addChild_(node)
	
	
def SampleScene_touchesBegan_withEvent_(_self, _cmd, _touches, event):
	touches = ObjCInstance(_touches)
	for t in touches:
		loc = t.locationInView_(skview)
		sz = ui.get_screen_size()
		# the following really should be an structure for quick lookup
		r = random.randint(0,10)
		if r == 0:
			addSpriteWithTexture(skview.scene(), 'emj:Dizzy', loc.x, sz.height, alpha =0.75)
		elif r == 1:
			addSpriteWithTexture(skview.scene(), 'emj:Anchor', loc.x, sz.height)
		elif r == 2:
			addSpriteWithTexture(skview.scene(), 'emj:Closed_Book', loc.x, sz.height)
		elif r == 3:
			addSpriteWithTexture(skview.scene(), 'plc:Character_Horn_Girl', loc.x, sz.height, True)
		elif r == 4:
			addSpriteWithTexture(skview.scene(), 'emj:Bomb', loc.x, sz.height)
		elif r == 5:
			addSpriteWithTexture(skview.scene(), 'emj:Panda_Face', loc.x, sz.height)
		elif r == 6:
			addSpriteWithTexture(skview.scene(), 'emj:Clock_8', loc.x, sz.height, alpha=0.5)
		elif r == 7:
			addSpriteWithTexture(skview.scene(), 'emj:Moon_5', loc.x, sz.height)
		elif r == 8:
			addSpriteWithTexture(skview.scene(), 'plf:Enemy_SlimeBlock', loc.x, sz.height)
		elif r == 9:
			addSpriteWithTexture(skview.scene(), 'plf:Tile_BoxCrate_single', loc.x, sz.height, keep_aspect=False)
		else:
			addSpriteWithTexture(skview.scene(), 'emj:Cookie', loc.x, sz.height)
		break
		
		
def createSampleScene(sz):
	methods = [SampleScene_touchesBegan_withEvent_]
	protocols = []
	SampleScene = create_objc_class('SampleScene', SKScene, methods=methods, protocols=protocols)
	scene = SampleScene.sceneWithSize_(sz)
	
	scene.backgroundColor = UIColor.grayColor()
	
	helloNode = SKLabelNode.labelNodeWithFontNamed_("Chalkduster")
	helloNode.text = "Tap To Drop!"
	helloNode.fontSize = 30;
	helloNode.position = CGPoint(sz.width/2, sz.height/2)
	scene.addChild_(helloNode)
	
	side_width = 10
	side_height = sz.height *0.8
	side_y = 0 + side_height/2
	side_x = 20
	addBorder(scene, side_x, side_y, side_width, side_height)
	addBorder(scene, sz.width-side_x, side_y, side_width, side_height)
	addBorder(scene, sz.width/2,side_width/2,sz.width,side_width)
	
	return scene
	
	
def createSKView(x,y,w=0,h=0, debug=True):
	global skview
	
	#print(ui.get_screen_size())
	#print(w)
	#print(h)
	if w == 0 or h == 0:
		sz = ui.get_screen_size()
		w = sz[0]
		h = sz[1]
	skview = SKView.alloc().initWithFrame_((CGRect(CGPoint(x, y), CGSize(w,h))))
	
	skview.showsFPS = debug
	skview.showsNodeCount = debug
	skview.showsPhysics = debug
	return skview
	
	
def CustomViewController_viewWillAppear_(_self, _cmd, animated):
	global scene
	z = ui.get_screen_size()
	sz = CGSize(z.width, z.height)
	scene = createSampleScene(sz)
	skview.presentScene_(scene)
	
	
def CustomViewController_viewWillDisappear_(_self, _cmd, animated):
	#print('disappear')
	skview.paused = True
	
	
@on_main_thread
def startGame():
	app = UIApplication.sharedApplication()
	root_vc = app.keyWindow().rootViewController()
	tabVC = root_vc.detailViewController()
	sz = tabVC.view().bounds()
	methods = [CustomViewController_viewWillAppear_, CustomViewController_viewWillDisappear_]
	protocols = []
	CustomViewController = create_objc_class('CustomViewController', UIViewController, methods=methods, protocols=protocols)
	cvc = CustomViewController.new().autorelease()
	skview = createSKView(0,0,sz.size.width,sz.size.height)
	cvc.view = skview
	cvc.title = 'SpriteKit'
	
	# this way you still have access to the console, can switch back to editor and kill
	# the tab; need a good way to close
	tabVC.addTabWithViewController_(cvc)
	
	# this way is painful to debug and crashes sometimes
	#root_vc.presentViewController_animated_completion_(cvc, True, None)
	# this way is also painful and need a good way to exit without killing the whole app
	#root_vc.showViewController_sender_(cvc, None)
	
if __name__ == '__main__':
	startGame()

