# https://gist.github.com/anonymous/f229353624df386c1beffb864dc2cce0

import ui
from timerview import TimerView

class StopWatch(TimerView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_start_time = 0
        self.value = 0
        self.state = 'stop'
        
    def draw(self):
        t0 = (self.value//(36000), self.value//600, self.value//10)
        t1 = (t0[0], t0[1]%60, t0[2]%60)
        ui.draw_string("{:02}:{:02}:{:02}".format(*t1),
            font=('Helvetica', 20),
            rect=(150, 0, 0, 0),
            color='black',
            alignment=ui.ALIGN_CENTER)
        
    def update(self):
        if self.state == 'run':
            self.value = int((self.start_time - self.current_start_time)*10)
        self.set_needs_display()


def button_action(sender):
    v1 = sender.superview['view1']    
    if sender.title == 'Reset':
        v1.value = 0
        v1.state = 'stop'
    elif sender.title == 'Start':
        v1.value = 0
        v1.current_start_time = v1.start_time
        v1.state = 'run'
    elif sender.title == 'Stop':
        v1.state = 'stop'
    
   
v = ui.load_view()
v.present('sheet')        
