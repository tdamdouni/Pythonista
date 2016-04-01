import scene

class MyClass(scene.Scene):
    def setup(self):
        self.rect2 = scene.Point(150,50)
        
    def draw(self):
        scene.background(0,0,1) # 0,0,1 = blue
        scene.fill(0,1,0)       # 0,1,0 = green
        scene.rect(50,50,50,50)
        scene.fill(1,0,0)       # 1,0,0 = red
        scene.rect(self.rect2.x,self.rect2.y,50,50)
    
    def touch_began(self,touch):
        if 50 < touch.location.x < 100 and 50 < touch.location.y < 100:
            if self.rect2.x < self.size.w - 100:
                self.rect2.x += 50

scene.run(MyClass())


