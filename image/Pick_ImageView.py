from __future__ import print_function
# https://forum.omz-software.com/topic/2335/display-image-from-photos-pick_image/8

# coding: utf-8

from scene import *
import photos

class MyScene(Scene):
    def __init__(self, mapimage):
        self.mapimage = mapimage.convert('RGBA')
        super(MyScene, self).__init__()

    def setup(self):
        self.mapimage = load_pil_image(self.mapimage)

    def draw(self):
        background(1, 1, .5)
        image(self.mapimage, 0, 0)
    
        # Draw a red circle for every finger that touches the screen:
        fill(1, 0, 0)
        for touch in self.touches.values():
            ellipse(touch.location.x - 50, touch.location.y - 50, 100, 100)
    
mapimage = photos.pick_image(show_albums=True)
if mapimage:
    scene = MyScene(mapimage)
    run(scene, frame_interval=1)
else:
    print('Canceled or invalid image.')