# Display the current clipboard text in full screen mode
import clipboard, console, scene
clipText = clipboard.get()
if not clipText:
    clipText = """Hang up your cellphone and drive your car!!!"""
zclipText = """Please take me home..."""

class MyScene(scene.Scene):
    def setup(self):
        (imageName, imageSize) = self.getImageNameAndSize()
        theRect = scene.Rect(0, 0, *imageSize)
        theRect.center(self.bounds.center())
        print(theRect), ; print(self.bounds)
        self.add_layer(scene.Layer(theRect))
        self.root_layer.image = imageName
        
    def getImageNameAndSize(self):
        for fontSize in xrange(256, 31, -32):
            (imageName, imageSize) = scene.render_text(clipText, font_size=fontSize)
            print(fontSize), ; print(imageSize), ; print(self.bounds)
            if scene.Point(*imageSize) in self.bounds:
                return (imageName, imageSize)
            scene.unload_image(imageName)
        return scene.render_text(clipText, font_size=12)
    
    def draw(self):
        #scene.background(0, 0, 0)
        self.root_layer.update(self.dt)
        self.root_layer.draw()
    
    def touch_began(self, touch):  pass
    def touch_moved(self, touch):  pass
    def touch_ended(self, touch):  pass

scene.run(MyScene(), orientation=scene.LANDSCAPE)
