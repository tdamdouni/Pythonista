import scene

class MyClass(scene.Scene): 
    def draw(self):
        # this method draws now 20 times per second the blue background
        scene.background(0,0,1) # 0,0,1 = blue

scene.run(MyClass(), frame_interval=3)  # 60 / 3 = 20fps -> see scene.run(...) for more details