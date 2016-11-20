[Share Code] Gestures for Pythonista
 
This is a convenience class for enabling gestures in Pythonista ui applications, including built-in views. Main intent here has been to make them Python friendly, hiding all the Objective-C stuff.

Get it from [GitHub](https://github.com/mikaelho/pythonista-gestures).
 
For example, do something when user swipes left on a TextView:
 
```
	def swipe_handler(view, swipe_start_location):
	    print ‘I was swiped, starting from ‘ + str(swipe_start_location)
	 
	tv = ui.TextView()
	Gestures().add_swipe(tv, swipe_handler, direction = Gestures.LEFT)
```
 
These gestures and methods are included:

* `add_tap(view, action, number_of_taps_required, number_of_touches_required)`
* `add_long_press(view, action, number_of_taps_required, number_of_touches_required, minimum_press_duration, allowable_movement)`
* `add_pan(view, action, minimum_number_of_touches, maximum_number_of_touches, set_translation)`
* `add_screen_edge_pan(view, action, edges)` (see below for possible `edges` values)
* `add_pinch(view, action)`
* `add_rotation(view, action)`
* `add_swipe(view, action, direction, number_of_touches_required)` (see below for possible `direction` values)
 
In all cases, only the `view` and `action` (event handler function like the `swipe_handler` in the example) are required. Refer to the UIKit UIGestureRecognizer [documentation](https://developer.apple.com/library/prerelease/ios/documentation/UIKit/Reference/UIGestureRecognizer_Class/index.html#//apple_ref/occ/cl/UIGestureRecognizer) on usage and default values.
 
Corresponding handler signatures are (representative names only, use whatever is convenient for you):

* `tap(view, location)` - same for long presses and swipes (where the location is the where the swipe began)
* `pan(view, location, absolute_translation, velocity)` - same for pans from the screen edges
* `pinch(view, location, scale, velocity)`
* `rotation(view, location, rotation, velocity)`
 
`scale`, `rotation` and `velocity` are numbers. `location` and `velocity` values are `ui.Point` instances with `x` and `y` members.
 
Possible screen edge pan `edges` values are (only one of these): `Gestures.EDGE_NONE`, `Gestures.EDGE_TOP`, `Gestures.EDGE_LEFT`, `Gestures.EDGE_BOTTOM`, `Gestures.EDGE_RIGHT`, `Gestures.EDGE_ALL`

Possible swipe `direction` values are (one or a list of these; if you need to know the actual swipe direction, add different directions as separate gestures):`Gestures.RIGHT`, `Gestures.LEFT`, `Gestures.UP`,`Gestures.DOWN`
 
All of the `add_x` methods return a `recognizer` object that can be used to remove or disable the gesture as needed:

* `remove(view, recognizer)`
* `disable(recognizer)`
* `enable(recognizer)`
 
You can also remove all gestures from a view with `remove_all_gestures(view)`.
 
__NOTES__:
 
* To facilitate the gesture handler callbacks from Objective-C to Python, the Gestures instance used to create the gesture must be live. You do not need to manage that as objc_util.retain_global is used to keep a global reference around. If you for some reason must track the reference manually, you can turn this behavior off with a `retain_global_reference=False` parameter for the constructor.
* Single Gestures instance can be used to add any number of gestures to any number of views, but you can just as well create a new instance whenever and wherever you need to add a new handler.
* If you need to create millions of dynamic gestures in a long-running app, it can be worthwhile to explicitly `remove` them when no longer needed, to avoid a memory leak.
