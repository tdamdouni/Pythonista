# https://gist.github.com/anonymous/7d1c9d06c7fd259c96118e51190f78ea

# https://forum.omz-software.com/topic/4500/presentation-timer

import ui, console

first_start_time = 15 # minutes

class Toucher(ui.View):

  seconds = 60
  start_time = first_start_time
  running = False
  current_time = first_start_time
  threshold = 60
  panning = False
  prev_y = 0
  start_loc = None

  def update(self):
    l.text = str(self.current_time)
    if self.current_time == 0:
      self.update_interval = 0
      self.running = False
      self.seconds = 60
      l.text_color = 'darkgrey'
      console.set_idle_timer_disabled(False)
      return
    self.seconds -= 1
    self.set_needs_display()
    if self.seconds == 0:
      self.seconds = 60
      self.current_time -= 1

  def draw(self):
    ui.set_color('black')
    path = ui.Path()
    path.line_width = 10
    path.move_to(0, self.height-5)
    path.line_to(self.width/60*self.seconds, self.height-5)
    path.stroke()

  def touch_began(self, touch):
    self.start_loc = touch.location
    self.panning = False
    self.prev_y = touch.location[1]

  def touch_moved(self, touch):
    (x,y) = touch.location
    if not self.panning:
      (px,py) = self.start_loc
      if abs(x-px)+abs(y-py) > 40:
        self.panning = True
        if self.prev_y == 0:
          self.prev_y = y
    if self.panning:
      if not self.running:
        delta_y = y - self.prev_y
        if abs(delta_y) > self.threshold:
          self.prev_y = y
          if delta_y > 0:
            self.current_time -= 1
          else:
            self.current_time += 1
          #if self.current_time > 15: self.current_time = 0
          if self.current_time < 0: 
            self.current_time = first_start_time
          l.text = str(self.current_time)
          self.seconds = 60
          self.set_needs_display()

  def touch_ended(self, touch):
    if not self.panning:
      self.running = self.running == False
      if self.running:
        self.update_interval = 1
        l.text_color = 'black'
        console.set_idle_timer_disabled(True)
      else:
        self.update_interval = 0
        l.text_color = 'darkgrey'
        console.set_idle_timer_disabled(False)
    self.panning = False
    self.prev_y = 0


l = ui.Label()
l.background_color = 'white'
l.text_color = 'darkgrey'
l.text = str(first_start_time)
l.alignment = ui.ALIGN_CENTER
l.font = ('Courier', int(max(ui.get_screen_size())/2.2))
l.touch_enabled = True

l.present('full_screen', hide_title_bar=True)

t = Toucher()
l.add_subview(t)
t.flex = 'WH'
t.frame = l.bounds

