'''
    create three background images in scene.setup() then in
    scene.draw() use the x coordinate of the user's drag
    location to determine which background image to display
'''

import scene
from PIL import Image, ImageDraw, ImageFont

theMessage = 'Drag the grey circle left and right to switch between the background images.'
fillColorRed    = (255, 0, 0, 255)
fillColorGreen  = (0, 255, 0, 255)
fillColorBlue   = (0, 0, 255, 255)
fillColorLtGrey = (192, 192, 192, 255)
theFont = ImageFont.truetype('Chalkduster', 24)

def oldMakeBgImage(inFillColor = fillColorBlue, inText = 'Blue'):
    img = Image.new("RGBA", (300,300))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0,0,200,200), fill=inFillColor)
    draw.text((65, 85), inText, fill=fillColorLtGrey,
                                font=theFont)
    del draw
    return scene.load_pil_image(img)
    
from contextlib import contextmanager

@contextmanager
def drawingContext(inImage):
    """Create an ImageDraw.Draw and then delete it when leaving the 'with' clause."""
    draw = ImageDraw.Draw(inImage)
    try:   yield draw
    finally: del draw

def makeBgImage(inFillColor = fillColorBlue, inText = 'Blue'):
    img = Image.new("RGBA", (300, 300))
    with drawingContext(img) as draw:
        draw.ellipse((0,0,200,200), fill=inFillColor)
        draw.text((65, 85), inText, fill=fillColorLtGrey,
                                    font=theFont)
    return scene.load_pil_image(img)

class MyScene(scene.Scene):
    def setup(self):
        self.bgImages = (
             makeBgImage(fillColorRed,   inText = 'Red'),
             makeBgImage(fillColorGreen, inText = 'Green'),
             makeBgImage(fillColorBlue,  inText = 'Blue'))
        self.sectionWidth = self.bounds.w / len(self.bgImages)
        self.tapLoc = self.bounds.center()
        self.bgIndex = 1

    def draw(self):
        scene.background(0.09,0.09,0.102)
        scene.image(self.bgImages[self.bgIndex],
                                     200, 300, 300, 300)
        scene.fill(0.3, 0.3, 0.3, 1)
        scene.no_stroke()
        scene.text(theMessage, font_name='Chalkduster',
                               font_size=22, alignment=9)
        scene.ellipse(self.tapLoc.x - 50,
                      self.tapLoc.y - 50, 100, 100)

    def touch_moved(self, touch):
        self.tapLoc = touch.location
        for i in xrange(len(self.bgImages)):
            if self.tapLoc.x <= (i + 1) * self.sectionWidth:
                self.bgIndex = i
                break

scene.run(MyScene(), scene.LANDSCAPE)
