# https://gist.github.com/cclauss/8683457
# Use PIL to draw an image of a diagonal line and then make a Pythonista scene.Layer to display the image.

import Image, ImageDraw, scene

def diagonalLineImage(inLength = 200, inColors = ('blue', 'ivory')):
    imageLength = inLength + 100  # the image can be larger than what you draw
    theImage = Image.new('RGBA', (imageLength, imageLength), inColors[1])
    draw = ImageDraw.Draw(theImage)
    draw.line((0, 0, inLength, inLength), fill = inColors[0])
    del draw
    return theImage

class DiagonalLineLayer(scene.Layer):
    def __init__(self):
        theImage = diagonalLineImage()
        theRect = scene.Rect(0, 0, *theImage.size)
        super(self.__class__, self).__init__(theRect)
        self.image = scene.load_pil_image(theImage)

class DiagonalLineScene(scene.Scene):
    def __init__(self):
        scene.run(self)

    def setup(self):
        self.layer = DiagonalLineLayer()
        self.add_layer(self.layer)
        self.layer.frame.center(self.bounds.center())

    def draw(self):
        scene.background(0.7, 0.7, 0.7)
        self.root_layer.update(self.dt)
        self.root_layer.draw()

DiagonalLineScene()