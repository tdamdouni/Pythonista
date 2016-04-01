import scene

class MyClass(scene.Scene):
    def setup(self):
        self.rect1 = scene.Rect(50,50,50,50)
        self.rect2 = scene.Rect(150,50,50,50)
        self.rect1_layer = scene.Layer(self.rect1)
        self.add_layer(self.rect1_layer)
        
    def draw(self):
        scene.background(0,0,1) # 0,0,1 = blue
        scene.fill(0,1,0)       # 0,1,0 = green
        scene.rect(*self.rect1) # *self.rect1 = self.rect1[0], ..., self.rect1[3]
        scene.fill(1,0,0)       # 1,0,0 = red
        scene.rect(*self.rect2)
    
    def touch_began(self,touch):
        if touch.layer == self.rect1_layer:
            if self.rect2.x < self.size.w - 100:
                self.rect2.x += 50

scene.run(MyClass())

# Example with layer. Compare it with beginner005-solution.py
# Add an additional layer for rect2 and change the size of rect2 while touching rect2
