import photos
import scene
import math

class PhotoText(scene.Scene):
    def __init__(self):
        self.distance_old = 0.0
        self.distance_new = 0.0
        self.distance_abs = 0.0
        self.reset = True
        self.zoom = 1.0        #no zoom
        self.zoom_min = 0.5
        self.zoom_max = 5
        self.zoom_speed = 3
        self.img2 = photos.pick_image()
        self.img = self.img2.convert('RGBA') #fix for current scene.load_pil_image()
        if self.img:
            self.picsize = scene.Size(*self.img.size)
            scene.run(self)
        else:
            print('Good bye!')
        
    def setup(self):
        self.layer = scene.Layer(self.bounds)
        self.layer.image = scene.load_pil_image(self.img)
        self.add_layer(self.layer)
        
    def draw(self):
        scene.background(0,0,0)
        self.root_layer.update(self.dt)
        self.root_layer.draw()
        scene.fill(1,1,1)   # watch+battery -> white background
        scene.rect(0, self.bounds.h, self.bounds.w, 20)  # watch+battery
        locations = [[0,0],[0,0]]
        i = 0
        if len(self.touches) == 2:
            for touch in self.touches.values():
                locations[i] = touch.location
                i += 1
            if self.reset:
                self.reset = False
                self.distance_old = math.sqrt(math.pow((locations[1][0] - locations[0][0]),2) + pow((locations[1][1] - locations[0][1]),2))
            else:
                self.distance_new = math.sqrt(math.pow((locations[1][0] - locations[0][0]),2) + pow((locations[1][1] - locations[0][1]),2))
                self.distance_abs = self.distance_new - self.distance_old
                self.reset = True
            if self.distance_abs != 0:
                zoom_new = self.distance_abs/self.bounds.w*self.zoom_speed
                if zoom_new < 0:
                    self.zoom += zoom_new
                else:
                    self.zoom += zoom_new
                if self.zoom < self.zoom_min:
                    self.zoom = self.zoom_min
                elif self.zoom > self.zoom_max:
                    self.zoom = self.zoom_max
                self.root_layer.animate('scale_x', self.zoom, duration=0.0)
                self.root_layer.animate('scale_y', self.zoom, duration=0.0)     

    def touch_ended(self,touch):
         self.reset = True
         
if photos.get_count():
    PhotoText()
else:
    print('Sorry no access or no pictures.')

# Additional tasks: 
# Optimize the code (could you move the touch code out of the draw method?)
# One finger moves the image section
# Rotating?
# ...
