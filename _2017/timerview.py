# https://gist.github.com/anonymous/f229353624df386c1beffb864dc2cce0

import ui, scene

class TimerView(ui.View):
    class TimerScene(scene.Scene):
        def update(self):
            self.view.superview.update()
            
    def create_sceneview(self):
        scene_view = scene.SceneView()
        scene_view.width = 0
        scene_view.height = 0
        scene_view.frame_interval = self.frame_interval
        scene_view.scene = TimerView.TimerScene()
        return scene_view
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_interval = kwargs.get('frame_interval', 1)
        self.add_subview(self.create_sceneview())
    
    @property    
    def start_time(self):
        return self.subviews[0].scene.t
        
    def draw(self):
        pass
        
    def update(self):  
        self.set_needs_display()
        
if __name__ == '__main__':
    from time import localtime
    class DigitalClock(TimerView):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        def draw(self):
            t = localtime()
            ui.draw_string("{:02}:{:02}:{:02}".format(
                t.tm_hour, t.tm_min, t.tm_sec),
                font=('Helvetica', 20),
                rect=(100, 100,0,0),
                alignment=ui.ALIGN_CENTER)
        
    v = DigitalClock(frame=(0,0,300, 300))
    v.present('sheet')
