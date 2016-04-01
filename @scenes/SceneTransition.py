# coding: utf-8

# https://forum.omz-software.com/topic/2500/scene-transitions

# Scene.present_modal_scene(other_scene)
# Present another scene on top of this one. This can be useful for overlay menus etc. While the scene is being presented, it receives all touch events.

#==============================

import scene

class OverlayScene(scene.Scene):
    def setup(self):
        self.background_color = 'midnightblue'
        scene.LabelNode(self.__class__.__name__, position=(self.size[0]/2, self.size[1]*0.9),
                            font=('Helvetica', self.size[0]/20), parent=self)

    def touch_ended(self, touch):
        self.dismiss_modal_scene()

class MainScene(scene.Scene):
    def __init__(self):
        scene.run(self)

    def setup(self):
        self.background_color = 'black'
        scene.LabelNode(self.__class__.__name__, position=(self.size[0]/2, self.size[1]*0.9),
                            font=('Helvetica', self.size[0]/20), parent=self)
        self.present_modal_scene(OverlayScene())

    def touch_ended(self, touch):
        if not self.presented_scene:
            self.present_modal_scene(OverlayScene())

if __name__ == '__main__':
    MainScene()