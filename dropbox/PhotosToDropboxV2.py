# coding: utf-8

# https://github.com/coomlata1/pythonista-scripts/blob/master/PhotosToDropbox.py

# https://forum.omz-software.com/topic/3299/get-filenames-for-photos-from-camera-roll/4

'''
#---Script: PhotosToDropbox.py
#---Author: @coomlata1
#---Created: 01/28/2015
#---Last Updated: 07/04/2016

This script now supports Pythonista 2.1 & the accompanying
changes to the 'Photo' module and requires Pythonista 2.1 or
greater.

This script and it's 2 pyui files, 'PhotosToDropbox.pyui' and
'PhotosToScale.pyui', will RESIZE, RENAME, GEO-TAG & UPLOAD
all selected photos in the iPhone camera roll to new folders
in your Dropbox account. The main folder will be named after
the year the photo was taken in the format 'yyyy', & the
subfolders will be named for the date the photo was created
in the format mm.dd.yyyy. The photos themselves will have the
exact time the photo was taken amended to the front of their
names in the format hh.mm.ss.XXXX.jpg, where XXXX is the
original name. All metadata in the original photo will be
copied to the resized & renamed copy in Dropbox if desired.
The script allows you to select your desired photo scaling
options.

This script requires that the pexif module, available at
https://github.com bennoleslie/pexif, be imported into
Pythonista. Just copy pexif.py into the Pythonista 'site
packages' dir. Pexif allows for both reading from and writing
to the metadata of image files. Many thanks to Ben Leslie for
maintaining the pexif module at github.

Script also requires DropboxLogin.py, available at https:/
gist.github.com/omz/4034526, which allows login access to
Dropbox.

The pyui interface dimensions were set up for an iPhone and
will need to be tweaked slightly to look good on an iPad.

Many thanks to @cclauss for excellent help and advice with
tightening the code and improving the program flow of the
script.
'''
from __future__ import print_function
import console
import location
import photos
from objc_util import ObjCInstance
import datetime
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
global ok

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
	global ok
	
	if sender.name == 'fifty':
		fifty = True
		v.close()
	if sender.name == 'custom':
		custom = True
		v.close()
	if sender.name == 'none':
		none = True
		v.close()
	if sender.name == 'ok_button':
		ok = True
		v2.close()
		
def get_date_time(d):
	# The defaults
	the_year = the_date = the_time = ''
	
	the_date = datetime.datetime.strftime(d,'%m.%d.%Y')
	the_time = datetime.datetime.strftime(d, '%H.%M.%S')
	the_year = datetime.datetime.strftime(d,'%Y')
	
	return the_year, the_date, the_time
	
def get_dimensions(asset, scale, img_name, min):
	# Original dimensions
	w = int(asset.pixel_width)
	h = int(asset.pixel_height)
	
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
	
def get_location(meta):
	if meta != None:
		# Dictionary of location data
		# ccc: pick results[0] right away
		results = location.reverse_geocode(meta)[0]
		
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
			
		# If name is an address then use street name only, because address is close but not always exact as to where location actually is.
		if find_number(name):
			name = street
			
		the_location = '{}, {} {} @ {}'.format(city, state, zipcode, name)
	else:
		the_location = ''
	return the_location
	
def find_number(a):
	return re.findall(r'^\.?\d+',a)
	
def get_degrees_to_rotate(d):
	if d == '1':
		degrees = 0
	elif d == '3':
		degrees = -180
	elif d == '6':
		degrees = -90
	elif d == '8':
		degrees = 90
	else:
		degrees = 0
		
	return degrees
	
def copy_meta(meta_src, meta_dst, x, y):
	'''
	Copy metadata from original photo to a resized photo that
	has no media metadata and write the results to a new photo
	that is resized with the media metadata.
	'''
	# Source photo
	img_src = pexif.JpegFile.fromFile(meta_src)
	# Destination photo
	img_dst = pexif.JpegFile.fromFile(meta_dst)
	img_dst.import_metadata(img_src)
	# Results photo
	'''
	After importing metadata from source we need to update the
	metadata to the new resize dimensions. Thanks to Ben Leslie
	for updating Pexif to accomodate this.
	'''
	img_dst.exif.primary.ExtendedEXIF.PixelXDimension = [x]
	img_dst.exif.primary.ExtendedEXIF.PixelYDimension = [y]
	
	# Now write the updated metadata to the resized photo
	img_dst.writeFile('meta_resized.jpg')
	
def timer(start, end, count, upload_pause):
	# Calculates the time it takes to run process, based on start and finish times
	# Add user defined time for each photo's dropbox upload pause
	elapsed  = (end - start) + (upload_pause * count)
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
	
def main(assets, keep_meta, geo_tag, dest_dir, size):
	minumum_size = True
	resizePercent = 0
	# This is time in seconds to allow for dropbox to process each photo.  Older iOS devices will require more time.
	upload_pause = 3
	
	if size == 'fifty':
		scale = float(50) / 100
	elif size == 'custom':
		scale = v2['scale_text']
		# Numbers only for textbox entries
		scale.keyboard_type = ui.KEYBOARD_NUMBER_PAD
		
		# Display ui locked in portrait orientation and wait till user selects something from it.
		v2.present(orientations = ['portrait'])
		v2.wait_modal()
		
		scale = float(scale.text) / 100
		# No minumums here...reduce all photos no matter what their size.
		minumum_size = False
		# If user pressed the close button then cancel script
		if not ok:
			sys.exit('Script Cancelled')
			
	elif size == 'none':
		scale = 1
		
	# Disable idle timer to cover working with a large batch of photos
	console.set_idle_timer_disabled(True)
	
	start = time.clock()
	
	# Create an instance of Dropbox client
	drop_client = get_client()
	
	for asset in assets:
		print('\nProcessing photo...')
		# Get date & time photo was taken
		the_year, the_date, the_time = get_date_time(asset.creation_date)
		
		file_name = ''
		# Formulate file name for photo
		old_filename = str(ObjCInstance(asset).filename())
		
		if the_date:
			folder_name = '{}/{}'.format(the_year, the_date)
			new_filename = '{}.{}'.format(the_time, old_filename)
		else:
			folder_name = 'NoDates'
			new_filename = old_filename
			keep_meta = False
			
		new_filename = '{}/{}/{}'.format(dest_dir, folder_name, new_filename)
		
		if folder_name == 'NoDates':
			no_exif.append(new_filename)
			
		file_name = '{}.{}'.format(the_time, file_name)
		
		# Get dimensions for resize based on size of original photo
		new_w, new_h, w, h, resizeOk = get_dimensions(asset, scale, new_filename, minumum_size)
		
		fmt = '\nOriginal Name: {}\nNew Name: {}'
		
		print(fmt.format(old_filename, new_filename))
		
		fmt = '\nOriginal Size: {}x{}\nNew Size: {}x{}'
		print(fmt.format(w, h, new_w, new_h))
		
		addToMsg = 'with' if keep_meta else 'without'
		
		if resizeOk:
			msg = '\nCreating resized copy of original photo {} the metadata from original.'
		else:
			msg = '\nCreating copy of original photo {} the metadata from original.'
			
		print(msg.format(addToMsg))
		
		# Fetch asset's image data & return it as a io.BytesIO object and then as a byte string
		img = asset.get_image_data(original = False).getvalue()
		# Write string image of original photo to Pythonista script dir
		with open('with_meta.jpg', 'wb') as out_file:
			out_file.write(img)
			
		# Open image, resize it, and write new image to scripts dir
		img = Image.open('with_meta.jpg')
		# Retrieve a number that represents the orientation of photo
		orientation = str(ObjCInstance(asset).orientation())
		
		# Landscape
		if orientation == '1' or orientation == '3':
			img = img.resize((new_w, new_h),Image.ANTIALIAS)
			# Occasionally metadata will say the photo orientation is 1 even though the width is less than the height of photo.
			if new_w < new_h:
				oriented = 'portrait'
			else:
				oriented = 'landscape'
		# Portrait
		elif orientation == '6' or orientation == '8':
			img = img.resize((new_h, new_w), Image.ANTIALIAS)
			oriented = 'portrait'
		# Unavailable
		else:
			img = img.resize((new_w, new_h),Image.ANTIALIAS)
			oriented = 'unknown'
			
		print('\nThe orientation for photo is {}.'.format(oriented))
		
		if geo_tag:
			# Get geo-tagging info
			the_location = get_location(asset.location)
			
			if the_location:
				print('\nGeo-tagging photo...')
				
				the_time = the_time.replace('.',':')
				the_location = '{} @ {} in {}'.format(the_date, the_time, the_location)
				'''
				Get degrees needed to rotate photo for it's proper
				orientation. See www.impulsesdventue.com/photoexif
				orientation.html for more details.
				'''
				degrees = get_degrees_to_rotate(orientation)
				
				# Rotate photo so tag is on bottom of photo regardless of orientation
				img = img.rotate(degrees).convert('RGBA')
				# Tuple
				w, h = img.size
				draw = ImageDraw.Draw(img)
				
				# Font for geo-tag will be 28 pt Helvetica
				fontsize = 28
				font = ImageFont.truetype('Helvetica', fontsize)
				y = h - 35
				
				# Put red text @ bottom left of photo
				draw.text((25, y), the_location,(255, 0, 0), font = font)
				
				# Rotate photo back to original position
				img = img.rotate(-degrees)
			else:
				print('\nNo gps metadata for photo.')
				no_gps.append(new_filename)
		else:
			print('\nPhoto will not be geo_tagged. Flag is set to false.')
			
		# Save new image
		img.save('without_meta.jpg')
		
		if keep_meta:
			'''
			Copy metadata from 'with_meta.jpg' to 'without_meta.jpg
			and call this reprocessed image file
			'meta_resized.jpg'.
			'''
			copy_meta('with_meta.jpg', 'without_meta.jpg', new_w, new_h)
			
			jpg_file = 'meta_resized.jpg'
			
		else:
			# Use resized photo that has not had metadata added back into it
			jpg_file = 'without_meta.jpg'
			
		print('\nUploading photo to Dropbox...')
		'''
		Upload resized photo with or without original metadata to
		Dropbox...use 'with' statement to open file so file
		closes automatically at end of 'with'.
		'''
		with open(jpg_file,'r') as img:
			response = drop_client.put_file(new_filename, img)
			
			# Give Dropbox server time to process...pause time is user defined.
			time.sleep(upload_pause)
		response = jpg_file = the_location = img = the_date = the_time = the_year = new_filename = old_filename = ''
		print('\nUpload successful.')
		
	finish = time.clock()
	print('{} photos processed in {}'.format(count, timer(start, finish, count, upload_pause)))
	
	if no_exif:
		print('\nPhotos with no DateTimeOriginal tag in their metadata and will need categorizing manually:')
		print('\n'.join(no_exif))
		
	if no_resize:
		print('\nPhotos that did not get resized because either you chose not to resize, or they were smaller than the minumum size of 1600x1200:')
		print('\n'.join(no_resize))
		
	if no_gps:
		print('\nPhotos that did not get geo-tagged because there was no gps info in the photo\'s metadata:')
		print('\n'.join(no_gps))
		
	# Re-enable idle timer
	console.set_idle_timer_disabled(False)
	
if __name__ == '__main__':
	console.clear()
	
	# Make sure photos are available...
	if len(photos.get_assets()) != 0:
		# Grab all photos in camera roll
		all_assets = photos.get_assets()
		# Allow multiple selects
		assets = photos.pick_asset(all_assets,title = 'Select Desired Photos', multi=True)
	else:
		sys.exit('Camera roll is empty.')
		
	# Where any photos selected?
	try:
		count = len(assets)
	except TypeError:
		sys.exit('No photos selected.')
		
	# Default pic sizes
	fifty = False
	custom = False
	none = False
	ok = False
	
	# Load pyui files
	v = ui.load_view('PhotosToDropbox')
	v2 = ui.load_view('PhotosToScale')
	
	meta = v['toggle_meta']
	geo = v['toggle_geotag']
	
	# Display ui locked in portrait orientation and wait till user makes choices or quits.
	v.present(orientations = ['portrait'])
	v.wait_modal()
	
	# Get user option choices for keeping metadata and geo_tagging photos
	meta = meta.value
	geo = geo.value
	dest_dir = v['photo_dir'].text
	
	# Go with default if textbox is blank
	if len(dest_dir) == 0:
		dest_dir = '/Photos'
	# Check syntax
	elif dest_dir[:1] != '/':
		dest_dir = '/' + dest_dir
		
	# If user pressed the close button then close any loaded views and cancel script
	if fifty == custom == none == False:
		v2.close()
		sys.exit('Script cancelled!')
		
	# Otherwise store resizing choice in a variable to pass to main()
	elif fifty:
		size = 'fifty'
	elif custom:
		size = 'custom'
	elif none:
		size = 'none'
		
	main(assets, meta, geo, dest_dir, size)

