# https://forum.omz-software.com/topic/3174/how-do-i-add-textures-to-sprites/14

from scene import *

class MyScene (Scene):
    def setup(self):
        self.background_color = 'green'

        self.spriteName = SpriteNode()

        self.spriteName.position = self.size / 2      
 
        self.spriteName.texture = Texture('plc:Gem_Blue')
        #self.spriteName.texture = Texture('canvas.png')
        #self.spriteName.texture = Texture('image000.jpg')
        self.add_child(self.spriteName)

run(MyScene())
