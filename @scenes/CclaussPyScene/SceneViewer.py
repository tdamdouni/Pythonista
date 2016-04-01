import scene, ui

class MyScene (scene.Scene):
    def draw (self):
        scene.background(0, 0, 0)
        scene.fill(1, 0, 0)
        for touch in self.touches.values():
            x, y = touch.location
            scene.ellipse(x - 50, y - 50, 100, 100)

class SceneViewer(ui.View):
    def __init__(self, in_scene):
        self.present('full_screen', hide_title_bar = True)
        scene_view = scene.SceneView(frame=self.frame)
        scene_view.scene = in_scene()
        self.add_subview(scene_view)
        self.add_subview(self.close_button())
    
    def close_action(self, sender):
        print('Closing...')
        self.close()

    def close_button(self):
        the_button = ui.Button(title='X')
        the_button.x = self.width - the_button.width
        the_button.y = the_button.height / 2
        the_button.action = self.close_action
        the_button.font=('<system-bold>', 20)
        return the_button

#scene.run(MyScene)
SceneViewer(MyScene)
