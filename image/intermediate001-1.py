from __future__ import print_function
# https://github.com/humberry/scene-tutorial/blob/master/intermediate001-1.py

# https://forum.omz-software.com/topic/2523/load-image-problem

import photos
import scene

class PhotoText(scene.Scene):
    def __init__(self):
        self.img2 = photos.pick_image()
        self.img = self.img2.convert('RGBA') #fix for current scene.load_pil_image()
        if self.img:
            self.picsize = scene.Size(*self.img.size)
            scene.run(self)
        else:
            print('Good bye!')

    def setup(self):
        self.layer = scene.Layer(self.bounds)
        self.layer.image = scene.load_pil_image(self.img)
        self.add_layer(self.layer)
        
    def draw(self):
        scene.background(0,0,0)
        self.root_layer.update(self.dt)
        self.root_layer.draw()
        scene.fill(1,1,1)   # watch+battery -> white background
        scene.rect(0, self.bounds.h, self.bounds.w, 20)  # watch+battery

if photos.get_count():
    PhotoText()
else:
    print('Sorry no access or no pictures.')