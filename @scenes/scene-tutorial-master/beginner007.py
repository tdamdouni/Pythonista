import scene
import sys

class MyClass(scene.Scene):
    def setup(self):
        self.rect1 = scene.Rect(50,50,50,50)
        self.circle2 = scene.Rect(150,50,50,50)
        self.rect1_layer = scene.Layer(self.rect1)
        self.rect1_layer.background = scene.Color(0,1,0)
        self.rect1_layer.animate('alpha', 0.0, duration=1.0, autoreverse=True, repeat=3) # alpha animation
        self.add_layer(self.rect1_layer)    # touch handling
        self.circle2_layer = scene.Layer(self.circle2)
        self.add_layer(self.circle2_layer)
        
    def draw(self):
        scene.background(0,0,1) # 0,0,1 = blue
        self.rect1_layer.update(self.dt)   # alpha animation
        self.rect1_layer.draw()            # alpha animation
        #scene.fill(0,1,0)       # 0,1,0 = green        #scene.ellipse(*self.rect1) # *self.rect1 = self.rect1[0], ..., self.rect1[3]
        scene.fill(1,0,0)       # 1,0,0 = red
        scene.ellipse(*self.circle2)
    
    def touch_began(self,touch):
        if touch.layer == self.rect1_layer:
            if self.circle2.x < self.size.w - 150:
                self.circle2.x += 50
        if touch.layer == self.circle2_layer:
            if self.circle2.w == 50:
                self.circle2.w,self.circle2.h = 100, 100
            else:
                self.circle2.w,self.circle2.h = 50,50

scene.run(MyClass())

# Please change rect1 to circle1, but don't change the alpha animation.
# Please animate the x and y scaling from 50 to 100 and back.
