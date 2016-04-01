import scene
import sys
import Image
import ImageDraw

class MyClass(scene.Scene):
    def setup(self):
        self.circle1 = scene.Rect(50,50,50,50)
        self.circle2 = scene.Rect(150,50,50,50)
        
        self.circle1_layer = scene.Layer(self.circle1)
        circle1 = Image.new('RGBA', (101,101))
        draw1 = ImageDraw.Draw(circle1)
        draw1.ellipse((0,0,100,100),fill=(0,255,0,255))
        self.circle1_layer.image = scene.load_pil_image(circle1)
        self.circle1_layer.animate('alpha', 0.0, duration=1.0, autoreverse=True, repeat=3) # alpha animation
        self.add_layer(self.circle1_layer)    # touch handling
        
        self.circle2_layer = scene.Layer(self.circle2)      
        circle2 = Image.new('RGBA', (101,101))
        draw2 = ImageDraw.Draw(circle2)
        draw2.ellipse((0,0,100,100),fill=(255,0,0,255))
        self.circle2_layer.image = scene.load_pil_image(circle2)
        self.circle2_layer.animate('scale_x', 2.0, duration=1.0, autoreverse=True, repeat=sys.maxint) # alpha animation
        self.circle2_layer.animate('scale_y', 2.0, duration=1.0, autoreverse=True, repeat=sys.maxint) # alpha animation
        #self.add_layer(self.circle2_layer)    #no touch handling
        
    def draw(self):
        scene.background(0,0,1) # 0,0,1 = blue
        self.circle1_layer.update(self.dt)   # alpha animation
        self.circle1_layer.draw()            # alpha animation
        self.circle2_layer.update(self.dt)   # scale animation
        self.circle2_layer.draw()            # scale animation
    
    def touch_began(self,touch):
        if touch.layer == self.circle1_layer:
            if self.circle2.x < self.size.w - 150:
                self.circle2.x += 50

scene.run(MyClass())

