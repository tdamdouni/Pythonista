# http://omz-forums.appspot.com/pythonista/post/5144563366756352

import random, scene

sizeInPixels = 100

def rectFromPt(inPoint):  # returns a scene.Rect centered on inPoint
	half = sizeInPixels / 2
	return scene.Rect(inPoint.x - half, inPoint.y - half, sizeInPixels, sizeInPixels)
	
class ImageLayer(scene.Layer):
	def __init__(self, inCenter, inImage):
		super(self.__class__, self).__init__(rectFromPt(inCenter))
		self.image = inImage
		
class MyScene(scene.Scene):
	def __init__(self):
		scene.run(self)  # a self running scene
		
	def setup(self):
		#centerOfScreen = self.bounds.center()
		thePoint = scene.Point(10 + sizeInPixels / 2, 10 + sizeInPixels / 2)
		images = 'Rabbit_Face Mouse_Face Cat_Face Dog_Face Octopus Bear_Face Chicken Cow_Face'
		images = images.split()
		for image in images:
			scene.load_image(image)
		images *= 2 # go from 8 images to 16
		random.shuffle(images)
		for image in images:
			self.add_layer(ImageLayer(thePoint, image))
			thePoint.x += 10 + sizeInPixels / 3
			thePoint.y = thePoint.x
		self.touchedLayer = None
		
	def draw(self):
		scene.background(0, 0, 0)
		self.root_layer.update(self.dt)
		self.root_layer.draw()
		
	def touch_began(self, touch):
		if touch.layer != self.root_layer:
			self.touchedLayer = touch.layer
			
	def touch_moved(self, touch):
		if self.touchedLayer:
			self.touchedLayer.frame = rectFromPt(touch.location)
			
	def touch_ended(self, touch):
		self.touchedLayer = None
		
MyScene()  # a self running scene

