#!python2
# coding: utf-8
#
# https://forum.omz-software.com/topic/3502/display-in-share-sheet-the-map-where-a-photo-has-been-taken
#
# Needs Python 2 because appex.get_image crashes in Python 3
#
# MKMapView part initially copied from OMZ MapView demo
#        https://gist.github.com/omz/451a6685fddcf8ccdfc5
# then "cleaned" to keep the easiest code as possible
#
# In appex mode, dezooming too much crashes, perhaps memory problem?
import console
import clipboard
from objc_util import *
import ctypes
import ui
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS
import appex
#import photos          # used to test in non-appex mode

class CLLocationCoordinate2D (Structure):
	_fields_ = [('latitude', c_double), ('longitude', c_double)]
class MKCoordinateSpan (Structure):
	_fields_ = [('d_lat', c_double), ('d_lon', c_double)]
class MKCoordinateRegion (Structure):
	_fields_ = [('center', CLLocationCoordinate2D), ('span', MKCoordinateSpan)]
	
def get_gps(image):
	gps_latitude      = None
	gps_latitude_ref  = None
	gps_longitude     = None
	gps_longitude_ref = None
	exif_info = image._getexif()                            # Extract exifs from photo
	if exif_info:
		for tag, value in exif_info.items():        # Loop on exifs of photo
			decoded = TAGS.get(tag, tag)                    # Exif code
			if decoded == "GPSInfo":                            # Exif is GPSInfo
				for t in value:                                         # Loop on sub-exifs
					sub_decoded = GPSTAGS.get(t, t)     # Sub-exif code
					if   sub_decoded == 'GPSLatitude':
						gps_latitude = value[t]
					elif sub_decoded == 'GPSLatitudeRef':
						gps_latitude_ref = value[t]
					elif sub_decoded == 'GPSLongitude':
						gps_longitude = value[t]
					elif sub_decoded == 'GPSLongitudeRef':
						gps_longitude_ref = value[t]
						
				if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
					lat = convert_to_degrees(gps_latitude)
					lat_lon_txt = str(lat)+gps_latitude_ref
					if gps_latitude_ref != "N":
						lat = 0 - lat
					lon = convert_to_degrees(gps_longitude)
					lat_lon_txt = lat_lon_txt+' - '+str(lon)+gps_longitude_ref
					if gps_longitude_ref != "E":
						lon = 0 - lon
					return lat, lon, lat_lon_txt
	return False,False,None
	
def convert_to_degrees(value):
	# convert the GPS coordinates d m s to degrees in float
	d0 = value[0][0]
	d1 = value[0][1]
	d = float(d0) / float(d1)
	
	m0 = value[1][0]
	m1 = value[1][1]
	m = float(m0) / float(m1)
	
	s0 = value[2][0]
	s1 = value[2][1]
	s = float(s0) / float(s1)
	
	return d + (m / 60.0) + (s / 3600.0)
	
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
		
	@on_main_thread
	def add_pin(self, lat, lon, title):
		'''Add a pin annotation to the map'''
		MKPointAnnotation = ObjCClass('MKPointAnnotation')
		coord = CLLocationCoordinate2D(lat, lon)
		annotation = MKPointAnnotation.alloc().init().autorelease()
		annotation.setTitle_(title)
		annotation.setCoordinate_(coord, restype=None, argtypes=[CLLocationCoordinate2D])
		self.mk_map_view.addAnnotation_(annotation)
		
	@on_main_thread
	def set_region(self, lat, lon, d_lat, d_lon, animated=False):
		'''Set latitude/longitude of the view's center and the zoom level (specified implicitly as a latitude/longitude delta)'''
		region = MKCoordinateRegion(CLLocationCoordinate2D(lat, lon), MKCoordinateSpan(d_lat, d_lon))
		self.mk_map_view.setRegion_animated_(region, animated, restype=None, argtypes=[MKCoordinateRegion, c_bool])
		
	def will_close(self):
		appex.finish()
		
def main():

	#----- Main process -----
	console.clear()
	
	if not appex.is_running_extension():
		#img = photos.pick_image()
		console.hud_alert('Must run in appex mod','error')
		return
	else:
		img = appex.get_image(image_type='pil')
		
	if img == None:
		console.alert('No image passed','','Ok',hide_cancel_button=True)
		return
		
	lat,lon, lat_lon_txt = get_gps(img)
	
	if not lat or not lon:
		console.alert('No GPS tags in image','','Ok',hide_cancel_button=True)
		return
		
	# Hide script
	back = MapView(frame=(0, 0, 540, 620))
	back.background_color='white'
	back.name = 'GPS = '+lat_lon_txt
	back.present('sheet', hide_title_bar=False)
	
	back.set_region(lat, lon, 0.05, 0.05, animated=True)
	back.add_pin(lat, lon,str((lat, lon)))
	
# Protect against import
if __name__ == '__main__':
	main()

