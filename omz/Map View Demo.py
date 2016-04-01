# coding: utf-8

# https://forum.omz-software.com/topic/1972/beta-fun-with-mapkit-and-objc_util

# https://gist.github.com/omz/451a6685fddcf8ccdfc5

# I've been experimenting a lot with the new objc_util module lately, and I thought I'd share a few more advanced examples. So here's the first...

# Please note that this relies on a couple of changes I made in the very latest build (uploaded about an hour ago), and it won't work in previous betas.

# → MapView Demo.py (Gist)

# The example shows how you can combine the ui and objc_util modules to create entirely new UI elements, in this case a "native" MapView (which has been a popular feature request).

# The MapView class should be usable pretty much like any other ui.View, but it doesn't implement all features of the underlying (fairly complex) MapKit APIs, so you might want to extend it, if you need things like satellite view etc.

# Some of the code is fairly advanced, and probably requires some low-level knowledge about the Objective-C runtime to understand completely. To support being notified about scroll/zoom events, it was necessary to create a new Objective-C class that acts as the MKMapView's delegate. Creating new Objective-C classes is quite difficult to get right, and unfortunately there isn't really a good way to make this easier. The rest of the code is hopefully easier to understand – the only other "special" thing is the use of structs that aren't supported directly by objc_util (CLLocationCoordinate2D etc.). This makes it necessary to specify the return/argument types of some method calls explicitly (via the new restype/argtypes keyword arguments).

# Note: I haven't tested this on a 32-bit device so far, and it's possible that some minor changes are needed to make it work on both architectures.

# Feel free to ask me if there's something you don't understand in the code.

# coding: utf-8

'''
NOTE: This requires the latest beta of Pythonista 1.6 (build 160022)

Demo of a custom ui.View subclass that embeds a native map view using MapKit (via objc_util). Tap and hold the map to drop a pin.

The MapView class is designed to be reusable, but it doesn't implement *everything* you might need. I hope that the existing methods give you a basic idea of how to add new capabilities though. For reference, here's Apple's documentation about the underlying MKMapView class: http://developer.apple.com/library/ios/documentation/MapKit/reference/MKMapView_Class/index.html

If you make any changes to the OMMapViewDelegate class, you need to restart the app. Because this requires creating a new Objective-C class, the code can basically only run once per session (it's not safe to delete an Objective-C class at runtime as long as instances of the class potentially exist).
'''

from objc_util import *
import ctypes
import ui
import location
import time
import weakref

# _map_delegate_cache is used to get a reference to the MapView from the (Objective-C) delegate callback. The keys are memory addresses of `OMMapViewDelegate` (Obj-C) objects, the values are `ObjCInstance` (Python) objects. This mapping is necessary because `ObjCInstance` doesn't guarantee that you get the same object every time when you instantiate it with a pointer (this may change in future betas). MapView stores a weak reference to itself in the specific `ObjCInstance` that it creates for its delegate.
_map_delegate_cache = weakref.WeakValueDictionary()

# Create a new Objective-C class to act as the MKMapView's delegate...
try:
	# If the script was run before, the class already exists.
	OMMapViewDelegate = ObjCClass('OMMapViewDelegate')
except:
	IMPTYPE = ctypes.CFUNCTYPE(None, c_void_p, c_void_p, c_void_p, c_bool)
	def mapView_regionDidChangeAnimated_imp(self, cmd, mk_mapview, animated):
		# Resolve weak reference from delegate to mapview:
		map_view = _map_delegate_cache[self].map_view_ref()
		if map_view:
			map_view._notify_region_changed()
	imp = IMPTYPE(mapView_regionDidChangeAnimated_imp)
	# This is a little ugly, but we need to make sure that `imp` isn't garbage-collected:
	ui._retain_me_mapview_delegate_imp1 = imp
	NSObject = ObjCClass('NSObject')
	class_ptr = c.objc_allocateClassPair(NSObject.ptr, 'OMMapViewDelegate', 0)
	selector = sel('mapView:regionDidChangeAnimated:')
	c.class_addMethod(class_ptr, selector, imp, 'v0@0:0@0B0')
	c.objc_registerClassPair(class_ptr)
	OMMapViewDelegate = ObjCClass('OMMapViewDelegate')

class CLLocationCoordinate2D (Structure):
	_fields_ = [('latitude', c_double), ('longitude', c_double)]
class MKCoordinateSpan (Structure):
	_fields_ = [('d_lat', c_double), ('d_lon', c_double)]
class MKCoordinateRegion (Structure):
	_fields_ = [('center', CLLocationCoordinate2D), ('span', MKCoordinateSpan)]

class MapView (ui.View):
	@on_main_thread
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		MKMapView = ObjCClass('MKMapView')
		frame = CGRect(CGPoint(0, 0), CGSize(self.width, self.height))
		self.mk_map_view = MKMapView.alloc().initWithFrame_(frame)
		flex_width, flex_height = (1<<1), (1<<4)
		self.mk_map_view.setAutoresizingMask_(flex_width|flex_height)
		self_objc = ObjCInstance(self)
		self_objc.addSubview_(self.mk_map_view)
		self.mk_map_view.release()
		self.long_press_action = None
		self.scroll_action = None
		#NOTE: The button is only used as a convenient action target for the gesture recognizer. While this isn't documented, the underlying UIButton object has an `-invokeAction:` method that takes care of calling the associated Python action.
		self.gesture_recognizer_target = ui.Button()
		self.gesture_recognizer_target.action = self.long_press
		UILongPressGestureRecognizer = ObjCClass('UILongPressGestureRecognizer')
		self.recognizer = UILongPressGestureRecognizer.alloc().initWithTarget_action_(self.gesture_recognizer_target, sel('invokeAction:')).autorelease()
		self.mk_map_view.addGestureRecognizer_(self.recognizer)
		self.long_press_location = ui.Point(0, 0)
		self.map_delegate = OMMapViewDelegate.alloc().init().autorelease()
		self.mk_map_view.setDelegate_(self.map_delegate)
		self.map_delegate.map_view_ref = weakref.ref(self)
		_map_delegate_cache[self.map_delegate.ptr] = self.map_delegate
	
	def long_press(self, sender):
		#NOTE: The `sender` argument will always be the dummy ui.Button that's used as the gesture recognizer's target, just ignore it...
		gesture_state = self.recognizer.state()
		if gesture_state == 1 and callable(self.long_press_action):
			loc = self.recognizer.locationInView_(self.mk_map_view)
			self.long_press_location = ui.Point(loc.x, loc.y)
			self.long_press_action(self)
	
	@on_main_thread
	def add_pin(self, lat, lon, title, subtitle=None, select=False):
		'''Add a pin annotation to the map'''
		MKPointAnnotation = ObjCClass('MKPointAnnotation')
		coord = CLLocationCoordinate2D(lat, lon)
		annotation = MKPointAnnotation.alloc().init().autorelease()
		annotation.setTitle_(title)
		if subtitle:
			annotation.setSubtitle_(subtitle)
		annotation.setCoordinate_(coord, restype=None, argtypes=[CLLocationCoordinate2D])
		self.mk_map_view.addAnnotation_(annotation)
		if select:
			self.mk_map_view.selectAnnotation_animated_(annotation, True)
	
	@on_main_thread
	def remove_all_pins(self):
		'''Remove all annotations (pins) from the map'''
		self.mk_map_view.removeAnnotations_(self.mk_map_view.annotations())
		
	@on_main_thread
	def set_region(self, lat, lon, d_lat, d_lon, animated=False):
		'''Set latitude/longitude of the view's center and the zoom level (specified implicitly as a latitude/longitude delta)'''
		region = MKCoordinateRegion(CLLocationCoordinate2D(lat, lon), MKCoordinateSpan(d_lat, d_lon))
		self.mk_map_view.setRegion_animated_(region, animated, restype=None, argtypes=[MKCoordinateRegion, c_bool])
	
	@on_main_thread
	def set_center_coordinate(self, lat, lon, animated=False):
		'''Set latitude/longitude without changing the zoom level'''
		coordinate = CLLocationCoordinate2D(lat, lon)
		self.mk_map_view.setCenterCoordinate_animated_(coordinate, animated, restype=None, argtypes=[CLLocationCoordinate2D, c_bool])
	
	@on_main_thread
	def get_center_coordinate(self):
		'''Return the current center coordinate as a (latitude, longitude) tuple'''
		coordinate = self.mk_map_view.centerCoordinate(restype=CLLocationCoordinate2D, argtypes=[])
		return coordinate.latitude, coordinate.longitude
	
	@on_main_thread
	def point_to_coordinate(self, point):
		'''Convert from a point in the view (e.g. touch location) to a latitude/longitude'''
		coordinate = self.mk_map_view.convertPoint_toCoordinateFromView_(CGPoint(*point), self._objc_ptr, restype=CLLocationCoordinate2D, argtypes=[CGPoint, c_void_p])
		return coordinate.latitude, coordinate.longitude
	
	def _notify_region_changed(self):
		if callable(self.scroll_action):
			self.scroll_action(self)


# --------------------------------------
# DEMO:

def long_press_action(sender):
	# Add a pin when the MapView recognizes a long-press
	c = sender.point_to_coordinate(sender.long_press_location)
	sender.remove_all_pins()
	sender.add_pin(c[0], c[1], 'Dropped Pin', str(c), select=True)
	sender.set_center_coordinate(c[0], c[1], animated=True)

def scroll_action(sender):
	# Show the current center coordinate in the title bar after the map is scrolled/zoomed:
	sender.name = 'lat/long: %.2f, %.2f' % sender.get_center_coordinate()

def main():
	# Create and present a MapView:
	v = MapView(frame=(0, 0, 500, 500))
	v.long_press_action = long_press_action
	v.scroll_action = scroll_action
	v.present('sheet')
	# Add a pin with the current location (if available), and zoom to that location:
	import location
	location.start_updates()
	time.sleep(1)
	loc = location.get_location()
	location.stop_updates()
	if loc:
		lat, lon = loc['latitude'], loc['longitude']
		v.set_region(lat, lon, 0.05, 0.05, animated=True)
		v.add_pin(lat, lon, 'Current Location', str((lat, lon)))

if __name__ == '__main__':
	main()
