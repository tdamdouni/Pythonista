# https://forum.omz-software.com/topic/3749/example-of-ui-and-classic-scene-render-loop/4

import scene, ui

class ChristmasScene(scene.Scene):
    def setup(self):
        scene.SpriteNode('emj:Christmas_Tree', anchor_point=(0, 0), parent=self)

view = scene.SceneView()
view.scene = ChristmasScene()
view.add_subview(ui.Button(title='Oh, Christmas Tree', center=view.center))
view.present()
