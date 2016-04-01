# http://omz-forums.appspot.com/pythonista/post/5246202996064256
# coding: utf-8
from scene import *

class MyScene (Scene):
    def draw(self):
        background(0, 0, 1)

view = SceneView()
view.scene = MyScene()
view.present('fullscreen', hide_title_bar=True)