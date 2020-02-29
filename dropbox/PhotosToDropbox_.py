#coding: utf-8

# https://github.com/coomlata1/pythonista-scripts/blob/master/PhotosToDropbox.py

# https://forum.omz-software.com/topic/3023/markdown-photo-upload

'''
PhotoToDropbox.py
@coomlata1

v1.0: 01/28/2015-Created

v1.1: 02/01/2015-Fixed bug in 'GetDimensions()'
function for square photos.

v1.2: 02/05/2015-Added code to geo-tag photos with
date, time, and place that photo was taken & a
timer function to track the processing time for
script.

v1.3: 02/09/2015-Reduced geo-tag font size for
smaller photos.

v1.4: 02/09/2015-Many thanks to cclaus for detailed
code cleanup & insightful comments.

v1.5: 02/22/2015-More code cleanup & better string
formatting

v1.6: 03/25/2015-Fixed bug in main()
where photo with no geotag was not being appended
to 'no_gps' list.

v1.7: 04/13/2015-Code tightening with help & thanks
to @cclauss.

v1.8: 08/20/2015-Fixed several bugs in geo-tag
function

v1.9: 01/01/2016-Resize photo before geo-tag stamp
rather than after, for more consistent placement &
font size for tag.

v2.0: 01/22/2016-Added code to disable auto timer
to prevent script from stalling on large photo transfers.
Inspiration for this comes from @cclauss.

v2.1: 01/30/2016-Added code and a pyui file to support
the selection of dropbox photo directory, sizing, geotag,
and metadata options via a form.

This Pythonista script will RESIZE,
RENAME, GEO-TAG & UPLOAD all selected
photos in the iPhone camera roll to new
folders in your Dropbox account. The main
folder will be named after the year the
photo was taken in the format 'yyyy', &
the subfolders will be named for the date
the photo was taken in the format
mm.dd.yyyy. The photos themselves will
have the exact time the photo was taken
amended to the front of their names in the
format hh.mm.ss.XXXX.jpg, where XXXX is
the original name. All metadata in the
original photo will be copied to the
resized & renamed copy if desired. The
script allows you to select your desired
photo scaling options.

Script requires that the pexif module,
available at https://github.com
bennoleslie/pexif, be imported into
Pythonista. Just copy pexif.py into the
Pythonista script dir. Pexif allows for
both reading from and writing to the
metadata of image files. Many thanks to
Ben Leslie for maintaining the pexif
module at github.

Script also requires DropboxLogin.py, available at
https://gist.github.com/omz/4034526, which allows
login access to dropbox.
'''
from __future__ import print_function
import console
import location
import photos
import re
import string
import sys
import time
import pexif
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from DropboxLogin import get_client
import ui

# Global variables for pyui file
global fifty
global custom
global none

# Global arrays for photos that will require manual processing
no_exif = []
no_resize = []
no_gps = []

# Global processing flags
resizeOk = True
minumum_size = True
resizePercent = 0

def button_tapped(sender):
	'@type sender: ui.Button'
	global fifty
	global custom
	global none
	
	if sender.name == 'fifty':
		fifty = True
		v.close()
	if sender.name == 'custom':
		custom = True
		v.close()
	if sender.name == 'none':
		none = True
		v.close()
		
def GetDateTime(meta):
	# The defaults
	theYear = theDate = theTime = ''
	# Added default
	exif = meta.get('{Exif}', None)
	if exif:
		try:
			theDate,theTime = str(exif.get('DateTimeOriginal')).split()
			theDate = theDate.split(':')
			theYear = theDate[0]
			theDate = '{}.{}.{}'.format(theDate[1],theDate[2],theYear)
			theTime = theTime.replace(':','.')
		except: # ccc: you should specify the errors you expect...
			pass  # https://realpython.com/blog/python/the-most-diabolical-python-antipattern
	return theYear, theDate, theTime
	
def GetDimensions(meta, scale, img_name, min):
	# Add default for exif
	exif = meta.get('{Exif}', None)
	#print exif
	# Original dimensions
	w = int(exif.get('PixelXDimension'))
	h = int(exif.get('PixelYDimension'))
	
	# Minumum dimensions
	min_w = 1600 if min else 0
	min_h = 1200 if min else 0
	
	if scale == 1:
		# If scaled at 100%...no resize
		no_resize.append(img_name)
		resizeOk = False
	# Square
	elif w == h:
	# Don't resize square photos with a height smaller than height of desired minumum size
		if h < min_h:
			no_resize.append(img_name)
			resizeOk = False
		else:
			resizeOk = True
	# Don't resize a non-square photo smaller than the desired minumum size.
	elif int(scale * (w)) * int(scale * (h)) < int(min_w * min_h):
		no_resize.append(img_name)
		resizeOk = False
	else:
		resizeOk = True
		
	new_w = int(scale * w) if resizeOk else w
	new_h = int(scale * h) if resizeOk else h
	
	# Return new & original dimensions, & resize flag
	return new_w, new_h, w, h, resizeOk
	
def CopyMeta(meta_src, meta_dst, x, y):
	'''
	Copy metadata from original photo to a
	resized photo that has no media metadata
	and write the results to a new photo
	that is resized with the media metadata.
	'''
	# Source photo
	img_src = pexif.JpegFile.fromFile(meta_src)
	# Destination photo
	img_dst = pexif.JpegFile.fromFile(meta_dst)
	img_dst.import_metadata(img_src)
	# Results photo
	'''
	After importing metadata from source
	we need to update the metadata to the
	new resize dimensions. Thanks to Ben
	Leslie for updating Pexif to
	accomodate this.
	'''
	img_dst.exif.primary.ExtendedEXIF.PixelXDimension = [x]
	img_dst.exif.primary.ExtendedEXIF.PixelYDimension = [y]
	
	# Now write the updated metadata to the resized photo
	img_dst.writeFile('meta_resized.jpg')
	
# ccc: rewrite to use dict.get() with default...returns degreesToRotate, orientation
def GetDegreesToRotate(d):
	rotate_dict = {'1':(0,'landscape'),
	'3':(-180,'landscape'),
	'6':(-90,'portrait'),
	'8': (90,'portrait')}
	return rotate_dict.get(str(d), (0, 'unknown'))
	
def GetLocation(meta):
	gps = meta.get('{GPS}', None)
	
	if gps:
		lat = gps.get('Latitude',0.0)
		lon = gps.get('Longitude',0.0)
		lat_ref = gps.get('LatitudeRef', '')
		lon_ref = gps.get('LongitudeRef', '')
		# Southern hemisphere
		if lat_ref == 'S':
			lat = -lat
		# Western hemisphere
		if lon_ref == 'W':
			lon = -lon
			
		coordinates = {'latitude':lat, 'longitude':lon}
		
		# Dictionary of location data
		# ccc: pick results[0] right away
		results = location.reverse_geocode(coordinates)[0]
		
		name = results['Name']
		try:
			street = results['Thoroughfare']
		except KeyError:
			street = ''
		try:
			city = results['City']
		except KeyError:
			city = ''
		try:
			state = results['State']
		except KeyError:
			state = ''
		try:
			zipcode = results['ZIP']
		except KeyError:
			zipcode = ''
			
		# If name is an address then use street name only
		if find_number(name):
			name = street
			
		theLocation = '{}, {} {} @ {}'.format(city, state, zipcode, name)
	else:
		theLocation = ''
		
	return theLocation
	
def find_number(a):
	return re.findall(r'^\.?\d+',a)
	
def Timer(start, end, count):
	"""
	Calculates the time it takes to run
	process, based on start and finish
	"""
	# Add 5 seconds to time for each photo's dropbox upload pause
	elapsed  = (end - start) + (5 * count)
	# Convert process time, if needed
	if elapsed < 60:
		time = '{:.2f}'.format(elapsed) + " seconds\n"
	elif elapsed < 3600:
		min = elapsed / 60
		time = '{:.2f}'.format(min) + " minutes\n"
	else:  # elapsed >= 3600:
		hour = elapsed / 3600
		time = '{:.2f}'.format(hour) + " hours\n"
		
	return time
	
def main(choose, keepMeta, geoTag, dest_dir, size):
	minumum_size = True
	resizePercent = 0
	
	if size == 'fifty':
		scale = float(50) / 100
	elif size == 'custom':
		msg = 'Enter desired reduction percent for selected photo(s): '
		try:
			scale = float(console.input_alert(msg,'Numbers only','35')) / 100
			# No minumums here...reduce all photos no matter what their size.
			minumum_size = False
		except KeyboardInterrupt:
			sys.exit('Script cancelled.')
	elif size == 'none':
		scale = 1
		
	#john = dialogs.form_dialog(title = 'Photo Options',fields=[{'type':'switch','title':'Geotag'}, {'type':'switch','title':'Keep Metadata'}])
	
	# Disable idle timer to cover working with a large batch of photos
	console.set_idle_timer_disabled(True)
	
	start = time.clock()
	
	# Create an instance of Dropbox client
	drop_client = get_client()
	
	ans = ''
	'''
	When metadata is returned with photo
	the photo is a tuple, with one the
	image, and the other the media
	metadata.
	'''
	for count, photo in enumerate(choose):
		# Raw data string and Metadata
		img, meta = photo
		#print meta
		#sys.exit()
		
		print('\nProcessing photo...')
		# Get date & time photo was taken
		theYear, theDate, theTime = GetDateTime(meta)
		
		# Formulate file name for photo
		old_filename = str(meta.get('filename'))
		
		if theDate:
			folder_name = '{}/{}'.format(theYear, theDate)
			new_filename = '{}.{}'.format(theTime, old_filename)
		else:
			folder_name = 'NoDates'
			new_filename = old_filename
			keepMeta = False
			
		new_filename = '{}/{}/{}'.format(dest_dir, folder_name, new_filename)
		
		if folder_name == 'NoDates':
			no_exif.append(new_filename)
			
		# Get dimensions for resize based on size of original photo
		new_w, new_h, w, h, resizeOk = GetDimensions(meta, scale, new_filename, minumum_size)
		
		fmt = '\nOriginal Name: {}\nNew Name: {}'
		
		print(fmt.format(old_filename, new_filename))
		
		fmt = '\nOriginal Size: {}x{}\nNew Size: {}x{}'
		print(fmt.format(w, h, new_w, new_h))
		
		addToMsg = 'with' if keepMeta else 'without'
		
		if resizeOk:
			msg = '\nCreating resized copy of original photo {} the metadata from original.'
		else:
			msg = '\nCreating copy of original photo {} the metadata from original.'
			
		print(msg.format(addToMsg))
		
		# Write string image of original photo to Pythonista script dir
		with open('with_meta.jpg', 'wb') as out_file:
			out_file.write(img)
			
		# Open image, resize it, and write new image to scripts dir
		img = Image.open('with_meta.jpg')
		img = img.resize((new_w, new_h),Image.ANTIALIAS)
		
		if geoTag:
			# Get geo-tagging info
			theLocation = GetLocation(meta)
			
			if theLocation:
				print('\nGeo-tagging photo...')
				
				# Find out if photo is oriented for landscape or portrait
				orientation = meta.get('Orientation')  # ccc: add a default?
				'''
				Get degrees needed to rotate photo
				for it's proper orientation. See
				www.impulsesdventue.com/photo
				exif-orientation.html for more
				details.
				'''
				degrees, oriented = GetDegreesToRotate(orientation)
				
				print('\nThe orientation for photo is {}.'.format(oriented))
				
				theTime = theTime.replace('.',':')
				theLocation = '{} @ {} in {}'.format(theDate, theTime, theLocation)
				
				# Rotate so tag is on bottom of photo regardless of orientation
				img = img.rotate(degrees).convert('RGBA')
				# Tuple
				w, h = img.size
				draw = ImageDraw.Draw(img)
				
				# Font for geo-tag will be 28 pt Helvetica
				#fontsize = 56 if w > 1300 else 28
				fontsize = 28
				font = ImageFont.truetype('Helvetica', fontsize)
				
				# Determine y axis for geotag
				#if h < 1000:
				#y = h - 35
				#else:
				#y = h - 75
				y = h - 35
				
				# Put red text @ bottom left of photo
				draw.text((25, y), theLocation,(255, 0, 0), font = font)
				
				# Rotate back to original position
				img = img.rotate(-degrees)
			else:
				print('\nNo gps metadata for photo.')
				no_gps.append(new_filename)
		else:
			print('\nPhoto will not be geotagged. Flag is set to false.')
			
		meta = ''
		#img = img.resize((new_w, new_h),Image.ANTIALIAS)
		# Save new image
		img.save('without_meta.jpg')
		
		if keepMeta:
			'''
			Copy metadata from 'with_meta.jpg'
			to 'without_meta.jpg and call this
			reprocessed image file
			'meta_resized.jpg'.
			'''
			CopyMeta('with_meta.jpg', 'without_meta.jpg', new_w, new_h)
			
			jpgFile = 'meta_resized.jpg'
			
		else:
			# Use resized photo that has not had metadata added back into it
			jpgFile = 'without_meta.jpg'
			
		print('\nUploading photo to Dropbox...')
		
		'''
		Upload resized photo with or without
		original metadata to Dropbox...use
		with statement to open file so file
		closes automatically at end of with.
		'''
		with open(jpgFile,'r') as img:
			response = drop_client.put_file(new_filename, img)
			
			# Give Dropbox server time to process
			time.sleep(5)
		response = jpgFile = theLocation = img = theDate = theTime = theYear = new_filename = old_filename = ''
		print('\nUpload successful.')
		
	finish = time.clock()
	print('{} photos processed in {}'.format(count + 1, Timer(start, finish, count + 1)))
	
	if no_exif:
		print('\nPhotos with no DateTimeOriginal tag in their metadata and will need categorizing manually:')
		print('\n'.join(no_exif))
		
	if no_resize:
		print('\nPhotos that did not get resized because either you chose not to resize, or they were smaller than the minumum size of 1600x1200:')
		print('\n'.join(no_resize))
		
	if no_gps:
		print('\nPhotos that did not get geo-tagged because there was no gps info in the photo\'s metadata:')
		print('\n'.join(no_gps))
		
if __name__ == '__main__':
	console.clear()
	# Make sure photos are available...
	if photos.get_count() != 0:
		'''
		Here we are picking photos from the
		camera roll which, in Pythonista,
		allows us access to extra media data
		in photo's metafile. Because raw data
		is set to true, the image is a string
		representing the image object, not the
		object itself.
		'''
		choose = photos.pick_image(show_albums = True, multi = True, original = True, raw_data = True,  include_metadata = True)
	else:
		sys.exit('No photos available.')
		
	photo_count = 0
	
	for count, photo in enumerate(choose):
		# Make sure a photo has been selected...Test first photo
		if photo_count < 1:
			try:
				# Raw data string and Metadata
				img, meta = photo
				# Increment counter
				photo_count = photo_count + 1
			# if we get an error there was no photo to test
			except TypeError:
				sys.exit('No photos selected.')
				
	# Default pic sizes
	fifty = False
	custom = False
	none = False
	
	# Load pyui file
	v = ui.load_view('PhotosToDropbox')
	
	meta = v['toggle_meta']
	geo = v['toggle_geotag']
	
	# Display ui and wait till user selects something from it
	v.present()
	v.wait_modal()
	
	# Get option choices for keeping metadata and geotagging photos
	meta = meta.value
	geo = geo.value
	dest_dir = v['photo_dir'].text
	
	# Go with default if textbox is blank
	if len(dest_dir) == 0:
		dest_dir = '/Photos'
	# Check syntax
	elif dest_dir[:1] != '/':
		dest_dir = '/' + dest_dir
		
	# If user pressed the close button then cancel script
	if fifty == custom == none == False:
		sys.exit('Script Cancelled')
	# Otherwise store resizing choice in a variable to pass to main()
	elif fifty:
		size = 'fifty'
	elif custom:
		size = 'custom'
	elif none:
		size = 'none'
		
	main(choose, meta, geo, dest_dir, size)

