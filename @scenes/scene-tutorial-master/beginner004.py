import scene

class MyClass(scene.Scene):
    def __init__(self):
        # good place to define/initialize variables
        # it's only called one time, when the Scene object is created
        pass
    
    def setup(self):
        # good place to define/initialize layers
        # it's only called one time, before the draw method is called
        pass
        
    def draw(self):
        scene.background(0,0,1) # 0,0,1 = blue
    
    def touch_began(self,touch):
        print('touch_began here x:{}, y:{}'.format(touch.location.x,touch.location.y))
    
    def touch_moved(self,touch):
        print('touch_moved there x:{}, y:{}'.format(touch.location.x,touch.location.y))
    
    def touch_ended(self,touch):
        print('touch_ended here x:{}, y:{}'.format(touch.location.x,touch.location.y))
        print

scene.run(MyClass())

# Please touch your display 3 times very quick and then quit the script. What do you see?
# Touch and move your finger only one time. What do you see?