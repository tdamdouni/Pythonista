# imageCongaLine.py
# A Conga line formed out of .png images inside Pythonista.app

import os, scene

imageWidth = 32

#print(os.getcwd())
os.chdir('../Documents')  # Look at files inside the app
#print(os.listdir('.'))

# print out all the .py files inside Pythonista.app
#fileExtension = '.py'  # '.txt'
#for fileName in os.listdir('.'):
#    if fileName.endswith(fileExtension):
#        print(fileName + '\n' + '=' * len(fileName))
#        with open(fileName) as fileHandle:
#            print(fileHandle.read() + '\n')
#sys.exit()

def getImageFunction():
    for fileName in os.listdir('.'):
        if fileName.endswith('@2x.png'):
            yield fileName
getImageName = getImageFunction()

class MovingImage(scene.Layer):
    def __init__(self, inImageName):
        theRect = scene.Rect(0, 0, imageWidth, imageWidth)
        scene.Layer.__init__(self, theRect)
        self.dx = self.dy = 2  # Initial direction: upperRight
        self.image = scene.load_image_file(inImageName)

    def move(self):
        self.frame.x += self.dx
        self.frame.y += self.dy
        sup = self.superlayer.frame
        if self.frame.x <= sup.x or (
           self.frame.x + self.frame.w >= sup.x + sup.w):
            self.dx = -self.dx           # change x direction
            self.frame.x += self.dx * 2  #  with a little hop
        if self.frame.y <= sup.y or (
           self.frame.y + self.frame.h >= sup.y + sup.h):
            self.dy = -self.dy           # change y direction
            self.frame.y += self.dy * 2  #  with a little hop

    def drop(self):
        self.dx = 0
        self.dy = -.5

class MyScene(scene.Scene):
    def setup(self):
        self.frameCount = 0

    def addMovingImage(self, inImageName):
        self.imageName = inImageName # .strip('@2x.pgn')
        theLayer = MovingImage(inImageName)
        theLayer.frame.center(self.bounds.center())
        theLayer.background = scene.Color(.1, .1, .1)
        self.add_layer(theLayer)
    
    def draw(self):
        if not self.frameCount % (imageWidth / 2):
            try:
                self.addMovingImage(getImageName.next())
            except StopIteration:
                self.imageName = None
                #for theLayer in self.root_layer.sublayers:
                #    if isinstance(theLayer, MovingImage):
                #        theLayer.drop()
        self.frameCount += 1
        scene.background(0, 0, 0)
        if self.imageName:
            scene.text(self.imageName, alignment=9)
        self.root_layer.update(self.dt)
        self.root_layer.draw()
        for theLayer in self.root_layer.sublayers:
            if isinstance(theLayer, MovingImage):
                theLayer.move()

    def touch_began(self, touch):  pass
    def touch_moved(self, touch):  pass
    def touch_ended(self, touch):  pass

scene.run(MyScene())
