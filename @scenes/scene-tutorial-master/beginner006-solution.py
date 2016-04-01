import scene

class MyClass(scene.Scene):
    def setup(self):
        self.rect1 = scene.Rect(50,50,50,50)
        self.rect2 = scene.Rect(150,50,50,50)
        self.rect1_layer = scene.Layer(self.rect1)
        self.add_layer(self.rect1_layer)
        self.rect2_layer = scene.Layer(self.rect2)
        self.add_layer(self.rect2_layer)
        
    def draw(self):
        scene.background(0,0,1) # 0,0,1 = blue
        scene.fill(0,1,0)       # 0,1,0 = green
        scene.rect(*self.rect1) # *self.rect1 = self.rect1[0], ..., self.rect1[3]
        scene.fill(1,0,0)       # 1,0,0 = red
        scene.rect(*self.rect2)
    
    def touch_began(self,touch):
        if touch.layer == self.rect1_layer:
            if self.rect2.x < self.size.w - 150:
                self.rect2.x += 50
        if touch.layer == self.rect2_layer:
            if self.rect2.w == 50:
                self.rect2.w,self.rect2.h = 100, 100
            else:
                self.rect2.w,self.rect2.h = 50,50

scene.run(MyClass())

