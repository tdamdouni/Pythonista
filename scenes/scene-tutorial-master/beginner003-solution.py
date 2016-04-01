import scene

class MyClass(scene.Scene):
    def draw(self):
        scene.background(0,0,1) # 0,0,1 = blue
        scene.stroke(1,0,0)       # 1,0,0 = red
        scene.stroke_weight(5)
        scene.line(50,50,100,50)
        scene.line(100,50,75,75)        scene.line(75,75,50,50)
scene.run(MyClass())
