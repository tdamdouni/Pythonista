# coding: utf-8

# https://github.com/coomlata1/pythonista-scripts

# Name: PhotoToDropbox.py
# Author: John Coomler
# v1.0: 01/28/2015-Created
# v1.1: 02/01/2015-Fixed bug in
# 'GetDimensions()' function for square
# photos.
# v1.2: 02/05/2015-Added code to geo-tag
# photos with date, time, and place that
# photo was taken & a timer function to
# track the processing time for script.
# v1.3: 02/09/2015-Reduced geo-tag font
# size for smaller photos.
# v1.4: 02/09/2015-Many thanks to cclaus
# for detailed code cleanup & insightful
# comments.
# v1.5: 02/22/2015-More code cleanup &
# better string formatting
# v1.6: 03/25/2015-Fixed bug in main()
# where photo with no geotag was not being
# appended to 'no_gps' list.
# v1.7: 04/13/2015-Code tightening with
# help & thanks to @cclauss.
'''
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

# Global arrays for photos that will require manual processing
no_exif = []
no_resize = []
no_gps = []

# Global processing flags
resizeOk = True

# Set this flag to false to resize photos without the metadata
keepMeta = True

# Set this flag to false to not stamp geo tags on photos
geoTag = True

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
    street = results['Thoroughfare']
    city = results['City']
    state = results['State']
    zipcode = results['ZIP']

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

def main():
  console.clear()
  try:
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
  except:
    sys.exit('No photos choosen...exiting.')

  minumum_size = True
  resizePercent = 0

  # Pick a scaling percent for selected photo(s)
  try:
    ans = console.alert('Reduce the selected photo(s) by what percent of their original size?', '', '50% with a 1600x1200 minumum', 'Custom without a minumum', 'None')

    if ans == 1:
      scale = float(50) / 100
    elif ans == 2:
      msg = 'Enter desired reduction percent for selected photo(s): '
      scale = float(console.input_alert(msg,'Numbers only','35')) / 100

      # No minumums here...reduce all photos no matter what their size.
      minumum_size = False
    elif ans == 3:
      # Don't resize
      scale = 1
  except (IndexError, ValueError):
    sys.exit('No valid entry...Process cancelled.')

  start = time.clock()

  # Create an instance of Dropbox client
  drop_client = get_client()

  ans = ''
  dest_dir = '/Photos'
  '''
  When metadata is returned with photo
  the photo is a tuple, with one the
  image, and the other the media
  metadata.
  '''
  for count,photo in enumerate(choose):
    print('\nProcessing photo...')
    # Raw data string and Metadata
    img, meta = photo
    #print meta
    #sys.exit()

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
        w, h= img.size
        draw = ImageDraw.Draw(img)
        '''
        Font for geo-tag of smaller photos
        will be 28 point Helvetica, while
        the rest will be 56 point.
        '''
        fontsize = 56 if w > 1200 else 28
        font = ImageFont.truetype('Helvetica', fontsize)

        # Put red text @ bottom left of photo
        draw.text((25, h-75), theLocation,(255, 0, 0), font = font)

        # Rotate back to original position
        img = img.rotate(-degrees)
      else:
        print('\nNo gps metadata for photo.')
        no_gps.append(new_filename)
    else:
      print('\nPhoto will not be geotagged. Flag is set to false.')

    meta = ''
    resized = img.resize((new_w, new_h),Image.ANTIALIAS)

    resized.save('without_meta.jpg')
    resized = ''

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
  main()

# - **PhotosToDropbox.py** - A script that lets you select multiple photos from the iPhone camera roll, resize & geo-tag them, and upload them to Dropbox where they are renamed and organized based on the date and time they were taken.  The cool part is that the script will preserve the metadata of the original photo if desired, using the [Pexif module](https://github.com/bennoleslie/pexif) to read the metadata from the original and write it back to the resized copy.  The Pexif module can be imported into Pythonista by simply copying pexif.py into the Pythonista script directory.