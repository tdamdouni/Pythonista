# coding: utf-8

# https://forum.omz-software.com/topic/2469/scene-gravity-and-orientation/3

# scene.gravity is deprecated - you should use motion.get_gravity instead, which is independent of the scene module.

# Basic usage looks like this:

import motion

motion.start_updates()
print(motion.get_gravity())
motion.stop_updates()

# All code that makes use of motion data needs to go between start_updates and stop_updates. If the code inside might raise an exception, you should put the entire thing in a try-finally block to make sure that motion updates are stopped so your battery doesn't drain too quickly.

import motion

motion.start_updates()
try:
    pass # Do motion things
finally:
    motion.stop_updates()

# The try block will not catch any exceptions, it only ensures that the finally block is run whether an exception is raised or not.

import scene
import motion


class MyScene (scene.Scene):
    def setup(self):
        self.label_node = scene.LabelNode('', ('Arial', 12), position=self.size*0.5, parent=self)
        motion.start_updates()
        self.orientation = '?'
        
    
    def update(self):
        x, y, z = motion.get_gravity()
        if abs(x) > abs(y):
            if x > 0:
                self.label_node.text = 'LANDSCAPE, RIGHT'
            else:
                self.label_node.text = 'LANDSCAPE, LEFT'
        else:
            if y < 0:
                self.label_node.text = 'PORTRAIT'
                
    def did_change_size(self):
        self.label_node.position = self.size*0.5
        
    def stop(self):
        motion.stop_updates()
        
scene.run(MyScene())