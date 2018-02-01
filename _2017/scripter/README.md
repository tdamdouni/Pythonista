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

# API

* [Class: Scripter](#class-scripter)
  * [Methods](#methods)
  * [Properties](#properties)
* [Functions](#functions)
  * [Script management](#script-management)
  * [Animation primitives](#animation-primitives)
  * [Animation effects](#animation-effects)
  * [Additional easing functions](#additional-easing-functions)


## Class: Scripter

Class that contains the `update` method used to run the scripts and to control their execution.

Runs at default 60 fps, or not at all when there are no scripts to run.

Inherits from ui.View; constructor takes all the same arguments as ui.View.

## Methods


#### ` update(self)`

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

#### ` pause_play_all(self)`

  Pause or play all animations. 

#### ` cancel(self, script)`

  Cancels any ongoing animations and
  sub-scripts for the given script. 

#### ` cancel_all(self)`

  Initializes all internal structures.
  Used at start and to cancel all running scripts.
### Properties


#### `default_update_interval (get, set)`


#### `default_fps (get, set)`

# Functions


#### SCRIPT MANAGEMENT
#### ` script(func)`

  Decorator for the animation scripts. Scripts can be functions, methods or generators.
  
  First argument of decorated functions must always be the view to be animated.
  
  Calling a script starts the Scripter `update` loop, if not already running.
  
  New scripts suspend the execution of the parent script until all the parallel scripts have
  completed, after which the `update` method will resume the execution of the parent script.

#### ` find_scripter_instance(view)`

  Scripts need a "controller" ui.View that runs the update method for them. This function finds 
  or creates the controller for a view as follows:
    
  1. Check if the view itself is a Scripter
  2. Check if any of the subviews is a Scripter
  3. Repeat 1 and 2 up the view hierarchy of superviews
  4. If not found, create an instance of Scripter as a hidden subview of the root view
  
  If you want cancel or pause scripts, and have not explicitly created a Scripter instance to 
  run them, you need to use this method first to find the right one.

#### ANIMATION PRIMITIVES
#### `@script timer(view, duration, action=None)`

  Acts as a wait timer for the given duration in seconds. `view` is only used to find the 
  controlling Scripter instance. Optional action function is called every cycle. 

#### `@script set_value(view, attribute, value, func=None)`

  Generator that sets the `attribute` to a `value` once, or several times if the value itself is a 
  generator or an iterator.
  
  Optional keyword parameters:
  
  * `func` - called with the value, returns the actual value to be set

#### `@script slide_value(view, attribute, end_value, target=None, start_value=None, duration=None, delta_func=None, ease_func=None, current_func=None, map_func=None)`

  Generator that "slides" the `value` of an
  `attribute` to an `end_value` in a given duration.
  
  Optional keyword parameters:
  
  * `start_value` - set if you want some other value than the current value of the attribute as the animation start value.
  * `duration` - time it takes to change to the target value. Default is 0.5 seconds.
  * `delta_func` - use to transform the range from start_value to end_value to something else.
  * `ease_func` - provide to change delta-t value to something else. Mostly used for easing; you can provide an easing function name as a string instead of an actual function. See supported easing functions [here](https://raw.githubusercontent.com/mikaelho/scripter/master/ease-functions.png).
  * `current_func` - Given the start value, delta value and progress fraction (from 0 to 1), returns the current value. Intended to be used to manage more exotic values like colors.
  * `map_func` - Used to translate the current value to something else, e.g. an angle to a Transform.rotation.

#### `@script slide_tuple(view, *args, **kwargs)`

  Slide a tuple value of arbitrary length. Supports same arguments as `slide_value`. 

#### `@script slide_color(view, attribute, end_value, **kwargs)`

  Slide a color value. Supports same
  arguments than `slide_value`. 

#### ANIMATION EFFECTS
#### `@script hide(view, **kwargs)`

  Fade the view away, then set as hidden 

#### `@script show(view, **kwargs)`

  Unhide view, then fade in. 

#### `@script pulse(view, color='#67cf70', **kwargs)`

  Pulses the background of the view to the given color and back to the original color.
  Default color is a shade of green. 

#### `@script move(view, x, y, **kwargs)`

  Move to x, y. 

#### `@script rotate(view, degrees, rps=1, start_value=0, **kwargs)`

  Rotate view given degrees at given rps - rounds per second. Set start_value if not
  starting from 0. 

#### `@script fly_out(view, direction, **kwargs)`

  Moves the view out of the screen in the given direction. Direction is one of the
  following strings: 'up', 'down', 'left', 'right'. 

#### `@script expand(view)`


#### ADDITIONAL EASING FUNCTIONS
#### ` jump(t)`

  Ease out "up" to 1, ease in back "down" to zero. 

#### ` drop_and_bounce(t, bounces=2, energy_conserved=0.4)`

  Easing function that can be used to simulate something that is dropped and bounces a few 
  times.
  
  Optional arguments:
    
  * `bounces` - how many times the value bounces before settling at target
  * `energy_conserved` - how high each bounce is compared to the previous bounce
