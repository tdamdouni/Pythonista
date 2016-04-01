# sounder.py
# play each of the .caf sounds inside the Pythonista.app

import os, os.path, scene, sound

framesPerSound = 60
pythonistaDir = os.path.expanduser('~/Pythonista.app')
#print(os.listdir(pythonistaDir))
soundFileExtention = '.caf'
wallpaperAppIcon = ('/AppIcon76x76@2x~ipad.png', '/AppIcon60x60@2x.png')

# print out all the .py files inside Pythonista.app
#fileExtension = '.py'  # '.txt'
#fileExtension = '.png'
#for fileName in os.listdir(pythonistaDir):
#    if fileName.endswith(fileExtension):
#        print(fileName + '\n' + '=' * len(fileName))
#        with open(fileName) as fileHandle:
#            print(fileHandle.read() + '\n')
#sys.exit()

def getSoundFunction():
    for fileName in os.listdir(pythonistaDir):
        if fileName.endswith(soundFileExtention):
            yield fileName.rstrip(soundFileExtention)
getSoundName = getSoundFunction()

def getWallpaper(inWallpaperFiles = wallpaperAppIcon):
    for wallpaperFile in inWallpaperFiles:
        wallpaperFile = pythonistaDir + wallpaperFile
        if os.path.isfile(wallpaperFile):  # does file exists?
            return scene.load_image_file(wallpaperFile)

class WallpaperLayer(scene.Layer):
    def __init__(self, inRect):
        super(self.__class__, self).__init__(inRect)
        self.image = getWallpaper()

def iPadScreen(inBounds): # Is screen larger than an iPhone?
    return min(inBounds.w, inBounds.h) > 350  # iPhone == 320

class MyScene(scene.Scene):
    def __init__(self):
        scene.run(self)

    def setup(self):
        self.frameCount = 0
        self.fontSize = 100 if iPadScreen(self.bounds) else 64
        self.add_layer(WallpaperLayer(self.bounds))

    def draw(self):
        if not self.frameCount % framesPerSound:
            try:
                self.soundName = getSoundName.next()
                #sound.load_effect(self.soundName)
                sound.play_effect(self.soundName)
            except StopIteration:
                self.soundName = None
        self.frameCount += 1
        scene.background(0, 0, 0)
        self.root_layer.update(self.dt)
        self.root_layer.draw()
        if self.soundName:
            x, y = self.bounds.center()
            scene.text(self.soundName, x=x, y=y, font_size=self.fontSize)

MyScene()
