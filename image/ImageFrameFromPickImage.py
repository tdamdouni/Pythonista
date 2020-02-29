from __future__ import print_function
# https://forum.omz-software.com/topic/2335/display-image-from-photos-pick_image/3

# coding: utf-8

from scene import *
import photos

class MyScene(Scene):   
    def __init__(self, mapimage):
        mapimage2 = mapimage.convert('RGBA')
        self.mapimage = load_pil_image(mapimage2)
        super(MyScene,self).__init__()

    def draw(self):
        # This will be called for every frame
        background(1, 1, .5)
        fill(1, 0, 0)
        
        image(self.mapimage, 0, 0)

        # Draw a red circle for every finger that touches the screen:
        for touch in self.touches.values():
            ellipse(touch.location.x - 50, touch.location.y - 50, 100, 100)

mapimage = photos.pick_image(show_albums=True)

if mapimage:
    scene = MyScene(mapimage)
    run(scene, frame_interval=1)
    mapimage2 = mapimage.convert('RGBA')
    mapimage.show()
    mapimage2.show()
else:
    print('Canceled or invalid image.')