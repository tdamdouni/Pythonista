#coding: utf-8

'''
# _SCRIPTER_ - Pythonista UI animations

![Logo](https://raw.githubusercontent.com/mikaelho/scripter/master/logo.jpg)

# Quick start

In order to start using the animation effects, just import scripter and call the effects as functions:

    from scripter import *
    
    hide(my_button)
    
Effects expect an active UI view as the first argument. This can well be `self` or `sender` 
where applicable.

If you want to create a more complex animation from the effects provided, combine them in a
script:
  
    @script
    def my_script():
      move(my_button, 50, 200)
      pulse(my_button, 'red')
      yield
      hide(my_button)
      
Scripts control the order of execution with `yield` statements. Here movement and a red 
pulsing highlight happen at the same time. After both actions are completed, `my_button` fades 
away.
        
Run scripter.py in Pythonista to see a demo of most of the available effects.
        
See the API documentation for individual effects and how to roll your own with `set_value`, 
`slide_value` and `timer`.

_Note_: As of Sep 15, 2017, ui.View.update is only available in Pythonista 3 beta.
'''

from ui import *
from types import GeneratorType, SimpleNamespace
from numbers import Number
from functools import partial
import time, math

#docgen: Script management

def script(func):
  '''
  Decorator for the animation scripts. Scripts can be functions, methods or generators.
  
  First argument of decorated functions must always be the view to be animated.
  
  Calling a script starts the Scripter `update` loop, if not already running.
  
  New scripts suspend the execution of the parent script until all the parallel scripts have
  completed, after which the `update` method will resume the execution of the parent script.
  '''
  
  def wrapper(view, *args, **kwargs):
    gen = func(view, *args, **kwargs)
    if not isinstance(gen, GeneratorType):
      return gen
    scr = find_scripter_instance(view)
    scr.view_for_gen[gen] = view
    scr.parent_gens[gen] = scr.current_gen
    if scr.current_gen != 'root':
      scr.standby_gens.setdefault(scr.current_gen, set())
      scr.standby_gens[scr.current_gen].add(gen)
      scr.deactivate.add(scr.current_gen)
    scr.activate.add(gen)
    scr.update_interval = scr.default_update_interval
    scr.running = True

    return gen
    
  return wrapper
 
def find_scripter_instance(view):
  '''
  Scripts need a "controller" ui.View that runs the update method for them. This function finds 
  or creates the controller for a view as follows:
    
  1. Check if the view itself is a Scripter
  2. Check if any of the subviews is a Scripter
  3. Repeat 1 and 2 up the view hierarchy of superviews
  4. If not found, create an instance of Scripter as a hidden subview of the root view
  
  If you want cancel or pause scripts, and have not explicitly created a Scripter instance to 
  run them, you need to use this method first to find the right one.
  '''
  while view:
    if isinstance(view, Scripter):
      return view
    for subview in view.subviews:
      if isinstance(subview, Scripter):
        return subview
    parent = view.superview
    if parent:
      view = parent
    else:
      break
  # If not found, create a new one as a hidden
  # subview of the root view
  scr = Scripter(hidden=True)
  view.add_subview(scr)
  return scr
 

class Scripter(View):
  
  '''
  Class that contains the `update` method used to run the scripts and to control their execution.
  
  Runs at default 60 fps, or not at all when there are no scripts to run.
  
  Inherits from ui.View; constructor takes all the same arguments as ui.View.
  '''

  global_default_update_interval = 1/60
  default_duration = 0.5
      
  def __init__(self, *args, **kwargs):
    super().__init__(self, *args, **kwargs)
    self.default_update_interval = Scripter.global_default_update_interval
    self.cancel_all()
    self.running = False
    self.time_paused = 0
  
  @property
  def default_update_interval(self):
    '''
    The running rate for the update method. Frames per second is here considered to be just an
    alternative way of setting the update interval, and this property is linked to
    `default_fps` - change one and the other will change as well.
    '''
    return self._default_update_interval
    
  @default_update_interval.setter
  def default_update_interval(self, value):
    self._default_update_interval = value
    self._default_fps = 1/value
  
  @property
  def default_fps(self):
    '''
    The running rate for the update method. Frames per second is here considered to be just an
    alternative way of setting the update interval, and this property is linked to
    `default_update_interval` - change one and the other will change as well.
    '''
    return self._default_fps
    
  @default_fps.setter
  def default_fps(self, value):
    self._default_fps = value
    self._default_update_interval = 1/value
  
  def update(self):
    '''
    Main Scripter animation loop handler, called by the Puthonista UI loop and never by your
    code directly.
    
    This method:
      
    * Activates all newly called scripts and suspends their parents.
    * Calls all active scripts, which will run to their next `yield` or until completion.
    * As a convenience feature, if a `yield` returns `'wait'` or a specific duration,
    kicks off a child `timer` script to wait for that period of time.
    * Cleans out completed scripts.
    * Resumes parent scripts whose children have all completed.
    * Sets `update_interval` to 0 if all scripts have completed.
    '''
    for gen in self.activate:
      self.active_gens.add(gen)
    for gen in self.deactivate:
      self.active_gens.remove(gen)
    self.activate = set()
    self.deactivate = set()
    gen_to_end = []
    for gen in self.active_gens:
      wait_time = None
      try:
        self.current_gen = gen
        wait_time = next(gen)
      except StopIteration:
        if gen not in self.deactivate:
          gen_to_end.append(gen)
      if wait_time is not None:
        if wait_time == 'wait':
          wait_time = self.default_duration
        if isinstance(wait_time, Number):
          timer(self.view_for_gen[gen], wait_time)
    self.current_gen = 'root'
    self.time_paused = 0
    for gen in gen_to_end:
      self.active_gens.remove(gen)
      parent_gen = self.parent_gens[gen]
      del self.parent_gens[gen]
      if parent_gen != 'root':
        self.standby_gens[parent_gen].remove(gen)
        if len(self.standby_gens[parent_gen]) == 0:
          self.active_gens.add(parent_gen)
          del self.standby_gens[parent_gen]
    if len(self.active_gens) == 0:
      self.update_interval = 0.0
      self.running = False

  def pause_play_all(self):
    ''' Pause or play all animations. '''
    self.update_interval = 0 if self.update_interval > 0 else self.default_update_interval
    self.running = self.update_interval > 0
    if not self.running:
      self.pause_start_time = time.time()
    else:
      self.time_paused = time.time() - self.pause_start_time

  def cancel(self, script):
    ''' Cancels any ongoing animations and
    sub-scripts for the given script. '''
    to_cancel = set()
    to_cancel.add(script)
    parent_gen = self.parent_gens[script]
    if parent_gen != 'root':
      self.standby_gens[parent_gen].remove(script)
      if len(self.standby_gens[parent_gen]) == 0:
        self.active_gens.add(parent_gen)
        del self.standby_gens[parent_gen]
    found_new = True
    while found_new:
      new_found = set()
      found_new = False
      for gen in to_cancel:
        if gen in self.standby_gens:
          for child_gen in self.standby_gens[gen]:
            if child_gen not in to_cancel: 
              new_found.add(child_gen)
              found_new = True
      for gen in new_found:
        to_cancel.add(gen)

    for gen in to_cancel:
      if gen == self.current_gen:
        self.currrent_gen = parent_gen
      del self.view_for_gen[gen]
      del self.parent_gens[gen]
      self.activate.discard(gen)
      self.deactivate.discard(gen)
      self.active_gens.discard(gen)
      if gen in self.standby_gens:
        del self.standby_gens[gen]

  def cancel_all(self):
    ''' Initializes all internal structures.
    Used at start and to cancel all running scripts.
    '''
    self.current_gen = 'root'
    self.view_for_gen = {}
    self.parent_gens = {}
    self.active_gens = set()
    self.standby_gens = {}
    self.activate = set()
    self.deactivate = set()
    self.running = False
  
  @staticmethod
  def _cubic(params, t):
    ''' Cubic function for easing animations '''
    ease_func_params = {
      'easeIn': (0, 0.05, 0.25, 1),
      'easeOut': (0, 0.75, 0.95, 1),
      'easeInOut': (0, 0.05, 0.95, 1),
      'easeOutIn': (0, 0.75, 0.25, 1),
      'easeInBounce': (0, -0.5, 0.25, 1),
      'easeOutBounce': (0, 0.75, 1.5, 1),
      'easeInOutBounce': (0, -0.5, 1.5, 1)
    }
    
    if isinstance(params, str):
      try:
        u = ease_func_params[params]
      except KeyError:
        raise ValueError('Easing function name must be one of the following: ' + ', '.join(list(ease_func_params)))
    else:
      u = params
    return u[0]*(1-t)**3 + 3*u[1]*(1-t)**2*t + 3*u[2]*(1-t)*t**2 + u[3]*t**3
  
#docgen: Animation primitives
  
@script
def timer(view, duration, action=None):
  ''' Acts as a wait timer for the given duration in seconds. `view` is only used to find the 
  controlling Scripter instance. Optional action function is called every cycle. '''
  
  scr = find_scripter_instance(view)
  start_time = time.time()
  dt = 0
  while dt < duration:
    if action: action(dt)
    yield
    if scr.time_paused > 0:
      start_time += scr.time_paused
    dt = time.time() - start_time
  
@script  
def set_value(view, attribute, value, func=None):
  '''
  Generator that sets the `attribute` to a `value` once, or several times if the value itself is a 
  generator or an iterator.
  
  Optional keyword parameters:
  
  * `func` - called with the value, returns the actual value to be set
  '''
    
  func = func if callable(func) else lambda val: val
  if isinstance(value, GeneratorType):
    while True:
      setattr(view, attribute, func(next(value)))
      yield
  elif hasattr(value, '__iter__') and not isinstance(value, str):
    iterator = iter(value)
    for value in iterator:
      setattr(view, attribute, func(value))
      yield
  else:
    setattr(view, attribute, func(value))

@script  
def slide_value(view, attribute, end_value, target=None, start_value=None, duration=None, delta_func=None, ease_func=None, current_func=None, map_func=None):
  '''
  Generator that "slides" the `value` of an
  `attribute` to an `end_value` in a given duration.
  
  Optional keyword parameters:
  
  * `start_value` - set if you want some other value than the current value of the attribute as the animation start value.
  * `duration` - time it takes to change to the target value. Default is 0.5 seconds.
  * `delta_func` - use to transform the range from start_value to end_value to something else.
  * `ease_func` - provide to change delta-t value to something else. Mostly used for easing; you can provide an easing function name as a string instead of an actual function. See supported easing functions [here](https://raw.githubusercontent.com/mikaelho/scripter/master/ease-functions.png).
  * `current_func` - Given the start value, delta value and progress fraction (from 0 to 1), returns the current value. Intended to be used to manage more exotic values like colors.
  * `map_func` - Used to translate the current value to something else, e.g. an angle to a Transform.rotation.
  '''
  scr = find_scripter_instance(view)
  duration = duration or scr.default_duration
  start_value = start_value if start_value is not None else getattr(view, attribute)
  
  delta_func = delta_func if callable(delta_func) else lambda start_value, end_value: end_value - start_value
  map_func = map_func if callable(map_func) else lambda val: val
  if isinstance(ease_func, str) or isinstance(ease_func, tuple):
    ease_func = partial(Scripter._cubic, ease_func)
  else:
    ease_func = ease_func if callable(ease_func) else lambda val: val
  current_func = current_func if callable(current_func) else lambda start_value, t_fraction, delta_value: start_value + t_fraction * delta_value
  
  delta_value = delta_func(start_value, end_value)
  start_time = time.time()
  dt = 0
  scaling = True
  while scaling:
    if dt < duration:
      t_fraction = ease_func(dt/duration)
    else:
      t_fraction = ease_func(1)
      scaling = False
    current_value = current_func(start_value, t_fraction, delta_value)
    setattr(view, attribute, map_func(current_value))
    yield
    if scr.time_paused > 0:
      start_time += scr.time_paused
    dt = time.time() - start_time

@script
def slide_tuple(view, *args, **kwargs):
  ''' Slide a tuple value of arbitrary length. Supports same arguments as `slide_value`. '''
  def delta_func_for_tuple(start_value, end_value):
    return tuple((end_value[i] - start_value[i] for i in range(len(start_value))))
  def current_func_for_tuple(start_value, t_fraction, delta_value):
    return tuple((start_value[i] + t_fraction * delta_value[i] for i in range(len(start_value))))
    
  delta_func = delta_func_for_tuple if 'delta_func' not in kwargs else kwargs['delta_func']
  current_func = current_func_for_tuple if 'current_func' not in kwargs else kwargs['current_func']
  
  return slide_value(view, *args, **kwargs, delta_func=delta_func, current_func=current_func)
  
@script
def slide_color(view, attribute, end_value, **kwargs):
  ''' Slide a color value. Supports same
  arguments than `slide_value`. '''
  start_value = kwargs.pop('start_value', None)
  if start_value:
    start_value = parse_color(start_value)
  end_value = parse_color(end_value)
  
  return slide_tuple(view, attribute, end_value, start_value=start_value, **kwargs)

#docgen: Animation effects

@script
def hide(view, **kwargs):
  ''' Fade the view away, then set as hidden '''  
  slide_value(view, 'alpha', 0.0, **kwargs)
  yield
  view.hidden = True

@script 
def show(view, **kwargs):
  ''' Unhide view, then fade in. '''
  view.alpha = 0.0
  view.hidden = False
  slide_value(view, 'alpha', 1.0, **kwargs)

@script
def pulse(view, color='#67cf70', **kwargs):
  ''' Pulses the background of the view to the given color and back to the original color.
  Default color is a shade of green. '''
  slide_color(view, 'background_color', color, ease_func=jump, **kwargs)
  
  '''
  orig_color = view.background_color
  slide_color(view, 'background_color', color, ease_func='easeOut')
  yield
  slide_color(view, 'background_color', orig_color, ease_func='easeIn')
  '''

@script    
def move(view, x, y, **kwargs):
  ''' Move to x, y. '''
  slide_value(view, 'x', x, **kwargs)
  slide_value(view, 'y', y, **kwargs)

@script    
def rotate(view, degrees, rps=1, start_value=0, **kwargs):
  ''' Rotate view given degrees at given rps - rounds per second. Set start_value if not
  starting from 0. '''
  duration = degrees / (rps * 360)
  radians = degrees/360*2*math.pi
  slide_value(view, 'transform', radians, start_value=start_value, map_func=lambda r: Transform.rotation(r), duration=duration, **kwargs)
  
@script
def fly_out(view, direction, **kwargs):
  ''' Moves the view out of the screen in the given direction. Direction is one of the
  following strings: 'up', 'down', 'left', 'right'. '''
  
  (sw,sh) = get_screen_size()
  (lx, ly, lw, lh) = convert_rect(rect=(0,0,sw,sh), to_view=view)
  (x,y,w,h) = view.frame
  targets = { 'up': ('y',ly-h), 'down': ('y',lh), 'left': ('x',lx-w), 'right': ('x',lw) }
  try:
    target_coord = targets[direction]
  except KeyError:
    raise ValueError('Direction must be one of ' + str(list(targets.keys())))
  slide_value(view, target_coord[0], target_coord[1], ease_func='easeIn', **kwargs)

@script
def expand(view):
  move(view, 0, 0)
  slide_value(view, 'width', view.superview.width)
  slide_value(view, 'height', view.superview.height)
  

#docgen: Additional easing functions

def jump(t):
  ''' Ease out "up" to 1, ease in back "down" to zero. '''
  if t < 0.5:
    t /= 0.5
    return Scripter._cubic('easeOut', t)
  else:
    t -= 0.5
    t /= 0.5
    return Scripter._cubic('easeIn', 1-t)

def drop_and_bounce(t, bounces=2, energy_conserved=0.4):
  '''
  Easing function that can be used to simulate something that is dropped and bounces a few 
  times.
  
  Optional arguments:
    
  * `bounces` - how many times the value bounces before settling at target
  * `energy_conserved` - how high each bounce is compared to the previous bounce
  '''
  slices = 2 * bounces + 1
  slice_duration = 1/slices
  slice_specs = []
  for s in range(slices):
    if t <= (s + 1) * slice_duration:
      slice_t = (t - s * slice_duration)/slice_duration
      height = energy_conserved**(math.ceil(s/2))
      if s % 2 == 0:
        # Down
        return (1-height) + Scripter._cubic('easeIn', slice_t) * height 
      else:
        # Up
        return 1 - Scripter._cubic('easeOut', slice_t) * height 
  return 1


if __name__ == '__main__':
  
  import editor
  
  class DemoBackground(View):
    
    def __init__(self):
      self.start_point = (0,0)
      self.axes_counter = 0
      self.curve_point_x = None
      self.curve_point_y = None
      self.curve = []
      self.hide_curve = False
    
    def draw(self):
      if self.axes_counter > 0:
        spx = self.start_point.x
        spy = self.start_point.y
        set_color('black')
        path = Path()
        path.move_to(spx, spy)
        path.line_to(spx+self.axes_counter, spy)          
        path.move_to(spx, spy)
        path.line_to(spx, spy-self.axes_counter)
        
        end_size = 10
        path.move_to(spx+self.axes_counter, spy)
        path.line_to(spx+self.axes_counter-end_size, spy-end_size)
        path.move_to(spx+self.axes_counter, spy)
        path.line_to(spx+self.axes_counter-end_size, spy+end_size)
        path.move_to(spx, spy-self.axes_counter)
        path.line_to(spx-end_size, spy-self.axes_counter+end_size)
        path.move_to(spx, spy-self.axes_counter)
        path.line_to(spx+end_size, spy-self.axes_counter+end_size)
        
        path.stroke()
        
        path = Path()
        set_color('#91cf96')
        path.move_to(spx, spy)
        
        if self.curve_point_x is not None:
          self.curve.append((spx+self.curve_point_x, spy-self.curve_point_y))
          
        if not self.hide_curve:
          for px, py in self.curve:
            path.line_to(px, py)

        path.stroke()
        
    def trigger_refresh(self, value):
      self.set_needs_display()
      return value
  
  v = DemoBackground()
  v.background_color = 'white'
  v.present('full_screen')
  
  class Demo(View):
    
    def __init__(self, *args, **kwargs):
      super().__init__(self, *args, *kwargs)
      self.frame = (100, 100, 150, 40)
      self.background_color = 'white'
      self.c = c = View(frame=(0,0,10,10))
      c.corner_radius = 5
      c.center = (15, 20)
      c.hidden = True
      c.background_color = 'black'
      self.l = l = Label(text='Scripter Demo')
      l.flex = 'WH'
      l.text_color = 'black'
      l.alignment = ALIGN_CENTER
      self.add_subview(c)
      self.add_subview(l)
      l.frame = self.bounds
      self.tv = tv = TextView(background_color='white')
      tv.text = editor.get_text()
      tv.text_color = '#4a4a4a'
      tv.frame = (2, 2, 146, 36)
      tv.flex = 'WH'
      tv.hidden = True
      self.add_subview(tv)
      self.hidden = True
      
    @script
    def demo_script(self):
      show(self)
      pulse(self, duration=1.0)
      yield
      yield 'wait'
      move(self, 200, 200)
      yield
      # Combine a primitive with a lambda and
      # target the contained Label instead of self
      set_value(self.l, 'text', range(1, 101), lambda count: f'Count: {count}')
      yield
      yield 'wait'
      # Transformations
      self.l.text = 'Rotating'
      rotate(self, 720, ease_func='easeInOutBounce')
      slide_color(self, 'background_color', 'green', duration=2.0)
      slide_color(self.l, 'text_color', 'white', duration=2.0)
      yield
      yield 'wait'
      self.l.text = 'Move two'
      # Create another view and control it as well
      # Use another function to control animation
      # "tracks"
      self.other = View(background_color='red', frame=(10, 200, 150, 40))
      v.add_subview(self.other)
      self.sub_script()
      move(self.other, 200, 400)
      yield
      self.l.text = 'Custom'
      yield 'wait'
      # Driving custom View.draw animation
      self.c.hidden = False
      slide_color(self, 'background_color', 'transparent')
      slide_color(self.l, 'text_color', 'black')
      v.start_point = SimpleNamespace(x=self.x+15, y=self.y+20)
      set_value(v, 'axes_counter', range(1, 210, 3), func=v.trigger_refresh)
      yield
      yield 'wait'
      slide_value(v, 'curve_point_x', 200, start_value=1, duration=2.0)
      slide_value(v, 'curve_point_y', 200, start_value=1, ease_func='easeInOutBounce', map_func=v.trigger_refresh, duration=2.0)
      yield
      yield 'wait'
      slide_value(self, 'x', self.x+200, duration=2.0)
      slide_value(self, 'y', self.y-200, ease_func='easeInOutBounce', duration=2.0)
      yield
      yield 'wait'
      self.l.text = 'Bounce'
      self.c.hidden = True
      slide_color(self, 'background_color', 'green')
      slide_color(self.l, 'text_color', 'white')
      slide_value(self, 'width', 76)      
      slide_value(self, 'height', 76)
      slide_value(self, 'corner_radius', 38)
      v.hide_curve = True
      v.set_needs_display()
      yield
      slide_value(self, 'x', v.start_point.x, ease_func='easeOut', duration=2.0)
      slide_value(self, 'y', v.start_point.y-self.height, ease_func=drop_and_bounce, duration=2.0)
      yield
      yield 1.0
      v.axes_counter = 0
      v.set_needs_display()
      self.c.hidden = True
      expand(self)
      slide_value(self, 'corner_radius', 0)
      slide_color(self, 'background_color', 'white')
      #self.border_color = 'green'
      #self.border_width = 2
      show(self.tv)
      slide_tuple(self.tv, 'content_offset', (0,0))
      yield
      yield 1.0
      slide_tuple(self.tv, 'content_offset', (0, self.tv.content_size[1]), duration=20)
      self.end_fade()
  
    @script
    def sub_script(self):
      move(self, 50, 200)
      yield
      move(self, 50, 400)        
      yield
      hide(self.other)
      fly_out(self.other, 'down')
      yield
      v.remove_subview(self.other)
      
    @script
    def end_fade(self):
      yield 7.0
      hide(v)
      
  
  s = Demo()
  v.add_subview(s)
  
  now_running = s.demo_script()
  scr = find_scripter_instance(s)
  
  def pause_action(sender):
    scr.pause_play_all()
    pause.title = 'Pause' if scr.running else 'Play'
  
  pause = Button(title='Pause')
  pause.frame = (v.width-85, 60, 75, 40)
  pause.background_color = 'black'
  pause.tint_color = 'white'
  pause.action = pause_action
  v.add_subview(pause)
  
  def cancel_demo(sender):
    scr.cancel(now_running)
    hide(pause)
    hide(sender)
    # or could just use
    # scr.cancel_all()
    # if clear that nothing else will be running
  
  b = Button(title='Cancel')
  b.frame = (v.width-85, 10, 75, 40)
  b.background_color = 'black'
  b.tint_color = 'white'
  b.action = cancel_demo
  v.add_subview(b)
