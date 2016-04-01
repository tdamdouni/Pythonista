import scene

class MyClass(scene.Scene): 
    def draw(self):
        # this method draws 60 times per second the blue background, if you don't change it
        scene.background(0,0,1) # 0,0,1 = blue

scene.run(MyClass())