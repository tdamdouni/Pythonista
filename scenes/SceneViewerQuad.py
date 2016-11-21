import scene, ui

colors = { 'red'   : (1, 0, 0),
           'green' : (0, 1, 0),
           'blue'  : (0, 0, 1),
           'white' : (1, 1, 1) }

class MyScene(scene.Scene):
    def __init__(self, in_dot_color = scene.Color(0, 0, 1)):
        super(self.__class__, self).__init__()
        self.dot_color = in_dot_color
        self.touch = None

    def draw(self):
        scene.background(0, 0, 0)
        if self.touch:
            scene.fill(*self.dot_color)
            x, y = self.touch.location
            scene.ellipse(x - 50, y - 50, 100, 100)

    def touch_began(self, touch):
        self.touch = touch

    def touch_moved(self, touch):
        self.touch = touch

    def touch_ended(self, touch):
        self.touch = None

class SceneViewer(ui.View):
    def __init__(self):
        self.present('full_screen', hide_title_bar = True)
        x, y = self.center
        rects = { 'red'   : (0, 0, x, y),
                  'green' : (x, 0, x, y),
                  'blue'  : (0, y, x, y),
                  'white' : (x, y, x, y) }
        for color in rects:
            scene_view = scene.SceneView(frame=rects[color])
            scene_view.scene = MyScene(colors[color])
            self.add_subview(scene_view)
        self.add_subview(self.close_button())
    
    def close_action(self, sender):
        #print('Closing...')
        self.close()
    
    def close_button(self):
        the_button = ui.Button(title='X')
        the_button.x = self.width - the_button.width
        the_button.y = the_button.height / 2
        the_button.action = self.close_action
        the_button.font=('<system-bold>', 20)
        return the_button

SceneViewer()
