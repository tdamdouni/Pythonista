import scene, threading, time

colorRed   = scene.Color(1, 0, 0)
colorGreen = scene.Color(0, 1, 0)
colorBlue  = scene.Color(0, 0, 1)
theColors  = (colorRed, colorGreen, colorBlue)

greyLight  = scene.Color(.7, .7, .7)
greyMedium = scene.Color(.5, .5, .5)
greyDark   = scene.Color(.3, .3, .3)
theGreys   = (greyLight, greyMedium, greyDark)

fmt = '{:<20} {}'

class MyScene(scene.Scene):
	def __init__(self, inFgColor = colorRed):
		self.fgColor = inFgColor
		
	def setup(self):
		# This will be called before the first frame is drawn.
		print(fmt.format('Scene setup:', self.fgColor))
		print(threading.active_count())
		
	def draw(self):
		# Called for every frame (typically 60 per second).
		scene.background(0, 0, 0)
		# Draw a circle for every finger touch
		scene.fill(*self.fgColor)
		for touch in self.touches.values():
			scene.ellipse(touch.location.x - 50,
			touch.location.y - 50, 100, 100)
			
	def touch_began(self, touch):  pass
	
	def touch_moved(self, touch):  pass
	
	def touch_ended(self, touch):  pass
	
	def pause(self):  # user pressed the home button
		print('pause({})'.format(self))
		
	def resume(self):
		print('resume({})'.format(self))
		
class ThreadClass(threading.Thread):
	def __init__(self, inFgColor):
		# Thread.__init__(self)
		# The following only works with single inheritance...
		super(self.__class__, self).__init__()
		self.fgColor = inFgColor
		print(fmt.format('Thread.__init__:', self.fgColor))
		
	def run(self):
		print(fmt.format('Thread scene starts:', self.fgColor))
		#scene.run(MyScene(self.fgColor))
		for i in xrange(5):  # interrupted sleep
			time.sleep(1)
		scene.run(MyScene(self.fgColor))  # Delayed 5 seconds
		print(fmt.format('Thread scene ends:', self.fgColor))
		
print('=' * 12)
print('Main starts.')
# Create three Scenes in Threads but delay calling run()
theThreads = [ThreadClass(theColor) for theColor in theColors]
for theThread in theThreads:
	theThread.start()
	
for theColor in theGreys:
	print(fmt.format('Main scene start:', theColor))
	theScene = MyScene(theColor)
	scene.run(theScene)
	print(fmt.format('Main scene end:', theColor))
	
print(threading.active_count())
for theThread in theThreads:
	print(threading.active_count())
	theThread.join()
	
print('Main ends.')

