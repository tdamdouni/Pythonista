import scene

class MyClass(scene.Scene):
    def draw(self):
        scene.background(0,0,1) # 0,0,1 = blue
        scene.fill(1,0,0)       # 1,0,0 = red
        scene.rect(50,50,50,50) # you like circles, try scene.ellipse(50,50,50,50)
        # Please draw a triangle with scene.line(...)
        # e.g. Point1: 50,50 Point2: 100,50 Point3: 75,75
        # scene.fill works only for rectangles and ellipses (hint: you need two other methods, see scene.line(...) for details

scene.run(MyClass())