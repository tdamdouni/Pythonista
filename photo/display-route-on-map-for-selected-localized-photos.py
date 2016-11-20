# coding: utf-8

# https://forum.omz-software.com/topic/3507/need-help-for-calling-an-objective_c-function/12

# todo
# - settîngs pin's visible or not
# - settings route color/width
# coding: utf-8
#
# MKMapView part initially copied from OMZ MapView demo
#        https://gist.github.com/omz/451a6685fddcf8ccdfc5
# then "cleaned" to keep the easiest code as possible
#
# For use of objc_util calls and crashes trace, more than help received from
#   @dgelssus and @JonB in Pythonista forum
#       https://forum.omz-software.com/topic/3507/need-help-for-calling-an-objective_c-function
#
# Display MKPolyline in Mapkit from Robert Kerr
#   http://blog.robkerr.com/adding-a-mkpolyline-overlay-using-swift-to-an-ios-mapkit-map/
#
import console
import clipboard
from objc_util import *
import ctypes
import ui
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS
import appex
import photos           # used to test in non-appex mode
import webbrowser # if the launcher app is installed

class CLLocationCoordinate2D (Structure):
	_fields_ = [('latitude', c_double), ('longitude', c_double)]
class MKCoordinateSpan (Structure):
	_fields_ = [('d_lat', c_double), ('d_lon', c_double)]
class MKCoordinateRegion (Structure):
	_fields_ = [('center', CLLocationCoordinate2D), ('span', MKCoordinateSpan)]
	
MKPolyline = ObjCClass('MKPolyline')
MKPolylineRenderer = ObjCClass('MKPolylineRenderer')

def mapView_rendererForOverlay_(self,cmd,mk_mapview,mk_overlay):
	try:
		overlay = ObjCInstance(mk_overlay)
		mapView = ObjCInstance(mk_mapview)
		if overlay.isKindOfClass_(MKPolyline):
			pr = MKPolylineRenderer.alloc().initWithPolyline(overlay);
			pr.strokeColor = UIColor.redColor().colorWithAlphaComponent(0.5);
			pr.lineWidth = 2;
			return pr.ptr
			pass
		return None
	except Exception as e:
		print('exception: ',e)
		
# Build method of MKMapView Delegate
methods = [mapView_rendererForOverlay_]
protocols = ['MKMapViewDelegate']
try:
	MyMapViewDelegate = ObjCClass('MyMapViewDelegate')
except:
	MyMapViewDelegate = create_objc_class('MyMapViewDelegate', NSObject, methods=methods, protocols=protocols)
	
class MapView(ui.View):

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
		
		# Set Delegate of mk_map_view
		self.map_delegate = MyMapViewDelegate.alloc().init().autorelease()
		self.mk_map_view.setDelegate_(self.map_delegate)
		
	@on_main_thread
	def add_pin(self, lat, lon, title):
		global all_points
		'''Add a pin annotation to the map'''
		MKPointAnnotation = ObjCClass('MKPointAnnotation')
		coord = CLLocationCoordinate2D(lat, lon)
		all_points.append(coord)            # store all pin's for MKPolyline
		annotation = MKPointAnnotation.alloc().init().autorelease()
		annotation.setTitle_(title)
		annotation.setCoordinate_(coord, restype=None, argtypes=[CLLocationCoordinate2D])
		self.mk_map_view.addAnnotation_(annotation)
		
	@on_main_thread
	def set_region(self, lat, lon, d_lat, d_lon, animated=False):
		'''Set latitude/longitude of the view's center and the zoom level (specified implicitly as a latitude/longitude delta)'''
		region = MKCoordinateRegion(CLLocationCoordinate2D(lat, lon), MKCoordinateSpan(d_lat, d_lon))
		self.mk_map_view.setRegion_animated_(region, animated, restype=None, argtypes=[MKCoordinateRegion, c_bool])
		
	@on_main_thread
	def addPolyLineToMap(self):
		global all_points
		global all_points_array
		all_points_array = (CLLocationCoordinate2D * len(all_points))(*all_points)
		polyline = ObjCInstance(MKPolyline.polylineWithCoordinates_count_(
		all_points_array,
		len(all_points),
		restype=c_void_p,
		argtypes=[POINTER(CLLocationCoordinate2D), c_ulong],
		))
		self.mk_map_view.addOverlay_(polyline)
		
	def will_close(self):
		# Back to home screen
		return # temporary during tests
		webbrowser.open('launcher://crash')
		
def main():
	global all_points
	
	#----- Main process -----
	console.clear()
	
	# Hide script
	back = MapView(frame=(0, 0, 540, 620))
	back.background_color='white'
	back.name = 'Display route of selected localized photos'
	back.present('full_screen', hide_title_bar=False)
	
	# Get a list of all photos
	c = photos.get_assets(media_type='image')
	# Pick at least two photos from all photos
	ps = photos.pick_asset(assets=c, title='Pick begin/end or all photos of the route', multi=True)
	if ps == None or len(ps) < 2:
		# Pick has been canceled
		console.hud_alert('At least two photos are needed','error')
		back.close()
		return
		
	# Loop on all photos
	route_points = []
	if len(ps) > 2: # more than 2 picked photos
		scan_ph = ps    # use picked photos only
	else:                       # 2 photos picked
		scan_ph = c     # scan all photos
		min_date = min(ps[0].creation_date,ps[1].creation_date).date()
		max_date = max(ps[0].creation_date,ps[1].creation_date).date()
	for p in scan_ph:
		p_date = p.creation_date.date()
		if (len(ps) > 2) or (len(ps) == 2 and p_date >= min_date and p_date <= max_date):
			# Photo belongs to the route period
			if p.location:
				# Photo has GPS tags
				lat = p.location['latitude']
				lon = p.location['longitude']
				# store latitude, longitude and taken date
				route_points.append((lat,lon,p_date))
				
	if len(route_points) < 2:
		console.hud_alert('At least two localized photos neded','error')
		back.close()
		return
	# Sort points by ascending taken date
	route_points = sorted(route_points,key = lambda x: x[2])
	# Compute min and max of latitude and longitude
	min_lat = min(route_points,key = lambda x:x[0])[0]
	max_lat = max(route_points,key = lambda x:x[0])[0]
	min_lon = min(route_points,key = lambda x:x[1])[1]
	max_lon = max(route_points,key = lambda x:x[1])[1]
	# Display map, center and zoom so all points are visible
	back.set_region((min_lat+max_lat)/2,(min_lon+max_lon)/2, 1.2*(max_lat-min_lat), 1.2*(max_lon-min_lon), animated=True)
	# Display pin's
	all_points = []
	for point in route_points:
		back.add_pin(point[0],point[1],str(point[2]))
		
	# Display polygon line of sorted locations
	back.addPolyLineToMap()
	
# Protect against import
if __name__ == '__main__':
	main()

