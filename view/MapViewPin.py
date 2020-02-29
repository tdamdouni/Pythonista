# coding: utf-8

# https://forum.omz-software.com/topic/2873/mapview-help/2

# coding: utf-8
# This has been derived for mapview example by Ole Zorn @omz url to come soon
from __future__ import print_function
import ui
import location
from objc_util import *

MKUserLocation = ObjCClass('MKUserLocation')
MKAnnotationView = ObjCClass('MKPinAnnotationView')
MKPointAnnotation = ObjCClass('MKPointAnnotation')
MKPinAnnotationView = ObjCClass('MKPinAnnotationView')

UIColor = ObjCClass('UIColor')
def mapView_viewForAnnotation_(self, cmd, mk_mapview, annotation):
	try:
		anno = ObjCInstance(annotation)
		mapView = ObjCInstance(mk_mapview)
		if anno.isKindOfClass_(MKPointAnnotation):
			pinView = mapView.dequeueReusableAnnotationViewWithIdentifier_('annoview')
			if not pinView:
				pinView = MKPinAnnotationView.alloc().initWithAnnotation_reuseIdentifier_(anno, 'annoview')
				pinView.canShowCallout = False
			else:
				pinView.annotation = anno
			return pinView
		return None
	except Exception as e:
		print(e)
		
methods = [mapView_viewForAnnotation_]
protocols = ['MKMapViewDelegate']
try:
	MyMapViewDelegate = ObjCClass('MyMapViewDelegate')
except:
	MyMapViewDelegate = create_objc_class('MyMapViewDelegate', NSObject, methods=methods, protocols=protocols)
	
	
	
class CLLocationCoordinate2D (Structure):
	_fields_ = [('latitude', c_double), ('longitude', c_double)]
	
class MapView (ui.View):
	@on_main_thread
	def __init__(self, *args, **kwargs):
		try:
			ui.View.__init__(self, *args, **kwargs)
			MKMapView = ObjCClass('MKMapView')
			frame = CGRect(CGPoint(0, 0), CGSize(self.width, self.height))
			self.mk_map_view = MKMapView.alloc().initWithFrame_(frame)
			flex_width, flex_height = (1<<1), (1<<4)
			self.mk_map_view.setAutoresizingMask_(flex_width|flex_height)
			self_objc = ObjCInstance(self)
			self_objc.addSubview_(self.mk_map_view)
			self.mk_map_view.release()
			self.map_delegate = MyMapViewDelegate.alloc().init().autorelease()
			self.mk_map_view.setDelegate_(self.map_delegate)
		except Exception as e:
			print(e)
			
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
		
if __name__ == '__main__':
	m = MapView()
	location.start_updates()
	loc = location.get_location()
	location.stop_updates()
	m.add_pin(lat = loc['latitude'], lon = loc['longitude'],title='Test')
	m.mk_map_view.setShowsUserLocation_(False)
	m.present()
	
#==============================

