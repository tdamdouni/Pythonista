# Toggle UI element subclass of Pythonista scene.Layer
# inspired by itsabouttime.py https://gist.github.com/upwart/9288979

from scene import *

class ToggleLayer(Layer):
    def __init__(self, parent = None , loc = None, size = 64, is_on = False):
        if loc:
            self.loc = loc
        elif parent:
            self.loc = parent.frame.center()
            self.loc.x -= size * 0.9
            self.loc.y -= size * 0.5
        else:
            self.loc = Point(10, 10)
        super(self.__class__, self).__init__(Rect(self.loc.x, self.loc.y, size * 1.8, size))
        if parent:
            parent.add_layer(self)
        self.size  = size
        self.is_on = is_on

    def toggle(self):
        self.is_on = not self.is_on
    
    def draw_on(self):
        (x, y) = self.loc
        line_width=self.size*0.1
        fill(0,1,0)
        stroke(0,1,0)
        stroke_weight(line_width)
        ellipse(x, y, self.size, self.size)
        rect(x+self.size/2, y, self.size-2*line_width, self.size)
        fill(0,0,0)
        ellipse(x+self.size-2*line_width, y, self.size, self.size)
        stroke(0,0,0)
        stroke_weight(line_width*0.8)
        line(x+self.size/2, y+self.size*0.25,
             x+self.size/2, y+self.size*0.75)

    def draw_off(self):
        (x, y) = self.loc
        line_width = self.size * 0.1
        fill(0,0,0)
        stroke(0.5,0.5,0.5)
        stroke_weight(line_width)
        ellipse(x+self.size-2*line_width, y, self.size, self.size)
        rect(x+self.size/2, y, self.size-2*line_width, self.size)
        stroke(0,0,0)
        rect(x+self.size/2,
             y+line_width,
             self.size/2+4*line_width,
             self.size-2*line_width)
        stroke(0.5,0.5,0.5)
        ellipse(x, y, self.size, self.size)
        stroke_weight(line_width*0.5)
        diameter=line_width*4
        ellipse(x+self.size+1*line_width,
                y+self.size*0.5-diameter/2,
                diameter, diameter)
        
    def draw(self, a=1.0):
        if self.is_on:
            self.draw_on()
        else:
            self.draw_off()

    def touch_began(self, touch):
        self.toggle()

class PanelLayer(Layer):
    def __init__(self, in_rect):
        super(self.__class__, self).__init__(in_rect)
        
    def draw(self, a=1.0):
        super(self.__class__, self).draw(a)
        tint(0.6, 0.6, 0.6)
        (x, y) = self.frame.center()
        text('Red\nGreen\nBlue', x=x-28, y=y, alignment=6, font_size=64)
            
class MyScene (Scene):
    def __init__(self):
        run(self)

    def setup(self):
        center = self.bounds.center()
        panel_layer = PanelLayer(Rect(0, 0, 320, 232))
        panel_layer.background = Color(1, 1, 1)
        panel_layer.frame.center(self.bounds.center())
        self.add_layer(panel_layer)
        self.toggle_red   = ToggleLayer(parent=panel_layer, loc=Point(10, 158))
        self.toggle_green = ToggleLayer(parent=panel_layer, loc=Point(10, 84))
        self.toggle_blue  = ToggleLayer(parent=panel_layer, loc=Point(10, 10), is_on=True)

    def draw(self):
        background(1 if self.toggle_red.is_on   else 0,
                   1 if self.toggle_green.is_on else 0,
                   1 if self.toggle_blue.is_on  else 0)
        self.root_layer.update(self.dt)
        self.root_layer.draw()

if __name__ == '__main__':
    MyScene()
