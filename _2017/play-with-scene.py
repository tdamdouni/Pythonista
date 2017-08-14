# https://forum.omz-software.com/topic/4143/how-do-i-do-to-play-the-movements-registered-in-the-scene/2

import scene

# for recording x and y...
points = []

class MyScene(scene.Scene):
    def __init__(self, in_dot_color=scene.Color(0, 0, 0, 1)):
        super().__init__()
        self.dot_color = in_dot_color
        self.touch = None
        
    def draw(self):
        scene.background(0, 0, 0)
        if self.touch:
            scene.fill('red')
            loc = self.touch.location
            scene.ellipse(loc.x - 50, loc.y - 50, 100, 100)
            scene.text('{}, {}'.format(*loc), 'Futura', 20, 100, 50)
            points.append(loc)  # is it be useful to check if loc == prev_loc?
        elif points:
            scene.fill('blue')
            for loc in points:
                scene.ellipse(loc.x - 50, loc.y - 50, 100, 100)
            
    def touch_began(self, touch):
        points.clear()
        self.touch = touch
        
    def touch_moved(self, touch):
        self.touch = touch
        
    def touch_ended(self, touch):
        self.touch = None

        
scene.run(MyScene(), show_fps=True)
