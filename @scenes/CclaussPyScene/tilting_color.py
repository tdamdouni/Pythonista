# tilting_color.py -- A gravity hack that uses Pythonista's motion.get_attitude() or
# scene.gravity() method to change screen colors when the user tilts their device.
# Red = abs(pitch), Green = abs(yaw), Blue = abs(roll)

import motion, scene

use_motion = True  # set to False to use scene.gravity()
 
fmt = """Tilt your device to change colors...
        x={}
        y={}
        z={}"""
 
class MyScene(scene.Scene):
    def __init__(self):  # This scene runs itself
        scene.run(self, frame_interval=15)  # Lower the FPS
        
    def setup(self):
        self.center = self.bounds.center()
        if use_motion:
            motion.start_updates()
    
    def stop(self):
        if use_motion:
            motion.stop_updates()
 
    def draw(self):
        x,y,z = motion.get_attitude() if use_motion else scene.gravity()
        r,g,b = abs(x), abs(y), abs(z)  # No negative colors
        scene.background(r, g, b)
        scene.tint(1-r, 1-g, 1-b)
        scene.text(fmt.format(x, y, z), font_size=32,
                   x=self.center.x, y=self.center.y)
 
MyScene()  # This scene runs itself
