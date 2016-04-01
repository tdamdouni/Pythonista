import scene

class MyClass(scene.Scene):
    def setup(self):
        self.color = 1      # 1 = green / 2 = red
        
    def draw(self):
        scene.background(0,0,1) # 0,0,1 = blue
        if self.color == 1:
            scene.fill(0,1,0)       # 0,1,0 = green
        elif self.color == 2:
            scene.fill(1,0,0)       # 1,0,0 = red
        scene.rect(50,50,50,50)
    
    def touch_began(self,touch):
        if 50 < touch.location.x < 100 and 50 < touch.location.y < 100:
            if self.color == 1:
                self.color = 2
            elif self.color == 2:
                self.color = 1

scene.run(MyClass())

# What do you expect when touching the green square?
# Rewrite the script to move a second square.
