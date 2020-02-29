# coding: utf-8

# https://github.com/coomlata1/pythonista-scripts

'''
#---Script: PhotosToDropbox.py
#---Author: @coomlata1
#---Created: 01/28/2015
#---Last Updated: 02/20/2017

#---Required: 1. Pythonista 2.1 or greater due to changes to 
    the 'Photo' module.
    2. The pexif module, available at
    https://github.com bennoleslie/pexif. It can be imported 
    into Pythonista. Just copy pexif.py into the Pythonista 
    'site packages' dir. Pexif allows for both reading from 
    and writing to the metadata of image files. Many thanks 
    to Ben Leslie for maintaining the pexif module at github.
    3. DropboxLogin.py, available at:
    https:/gist.github.com/omz/4034526, which allows login 
    access to Dropbox.
  
#---Purpose: This script will RESIZE, RENAME, GEO-TAG & 
    UPLOAD all selected photos in the iPhone camera roll to 
    new folders in your Dropbox account. The main folder will 
    be named after the year the photo was created in the 
    format 'yyyy', & the subfolders will be named for the 
    date the photo was created in the format mm.dd.yyyy. The 
    photos themselves will have the exact time the photo was 
    created amended to the front of their names in the format 
    hh.mm.ss.XXXX.jpg, where XXXX is the original name. All 
    metadata in the original photo will be copied to the 
    resized & renamed copy in Dropbox if desired. The script 
    allows you to select your desired photo scaling options.
    
#---To Do: Ui dimensions were set up for an iPhone and
    will need to be tweaked slightly to look good on an iPad. 

#---Kudos: Many thanks to @cclauss for excellent help and
    advice with tightening the code and improving the program 
    flow of the script. Thanks also to @JonB, @omz, & @cvp 
    for help via the Pythonista forum with getting the code 
    to work with the changes in the Photos module in 
    Pythonista 2.1.
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

# Globals for ui controls
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

# Determine which device by screen size
def is_iP6p():
  iP6p = True
  min_screen_size = min(ui.get_screen_size())

  #print min_screen_size
  #iphone6 min = 414
  #iphone6 max = 736
  #iphone5 min = 320
  #iphone5 max = 568

  if min_screen_size < 414:
    iP6p = False
  return iP6p
  
def button_tapped(sender):
  '@type sender: ui.Button'
  global fifty
  global custom
  global none
  global ok
  
  if sender.name == 'fifty':
    fifty = True
    v1.close()
  if sender.name == 'custom':
    custom = True
    v1.close()
  if sender.name == 'none':
    none = True
    v1.close()
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
    results = location.reverse_geocode(meta)[0]

    name = results['Name']
    
    street = results.get('Thoroughfare', '')
    city = results.get('City', '')
    state = results.get('State', '')
    zipcode = results.get('ZIP', '')
    
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
  #return degrees
  return {'1': 0, '3': -180, '6': -90, '8': 90}.get(d, 0)
    
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
  
# The ui
v1 = ui.View(name = 'PhotosToDropbox')
v2 = ui.View(name = 'PhotosToScale')

width, height = ui.get_screen_size()

if is_iP6p():
  v1.frame = v2.frame = (0, 0, width, height)
else:
  v1.frame = v2.frame = (0, 0, 414, 736)

v1.flex = v2.flex = 'WHLRTB'
v1.background_color = v2.background_color = 'cyan'

# Controls for v1
sw1 = ui.Switch(frame = (269, 172, 51, 31))
sw1.value = True
sw1.flex = 'WHLRTB'
sw1.action = button_tapped
sw1.name = 'toggle_meta'
v1.add_subview(sw1)

sw2 = ui.Switch(frame = (269, 224, 51, 31))
sw2.value = True
sw2.flex = 'WHLRTB'
sw2.action = button_tapped
sw2.name = 'toggle_geotag'
v1.add_subview(sw2)

btn1 = ui.Button(frame = (63, 362, 292, 59))
btn1.font = ('<system-bold>', 15)
btn1.flex = 'HLRTB'
btn1.border_width = 2
btn1.tint_color = 'black'
btn1.background_color = '#7af685'
btn1.action = button_tapped
btn1.title = '50% with a 1600x1200 minumum'
btn1.name = 'fifty'
v1.add_subview(btn1)

btn2 = ui.Button(frame = (63, 429, 292, 59))
btn2.font = ('<system-bold>', 15)
btn2.flex = 'HLRTB'
btn2.border_width = 2
btn2.tint_color = 'black'
btn2.background_color = '#7af685'
btn2.action = button_tapped
btn2.title = 'Custom % without a minumum'
btn2.name = 'custom'
v1.add_subview(btn2)

btn3 = ui.Button(frame = (63, 496, 292, 59))
btn3.font = ('<system-bold>', 15)
btn3.flex = 'HLRTB'
btn3.border_width = 2
btn3.tint_color = 'black'
btn3.background_color = '#7af685'
btn3.action = button_tapped
btn3.title = 'Keep Original Size'
btn3.name = 'none'
v1.add_subview(btn3)

tf1 = ui.TextField(frame =(251, 107, 104, 37))
tf1.font = ('<system-bold>', 17)
tf1.flex = 'HLRTB'
tf1.alignment = ui.ALIGN_LEFT
tf1.border_width = 2
tf1.text = '/Photos'
v1.add_subview(tf1)

lb1 = ui.Label(frame = (63, 285, 292, 69))
lb1.font = ('<system-bold>', 18)
lb1.flex = 'LRTB'
lb1.alignment = ui.ALIGN_CENTER
lb1.number_of_lines = 0
lb1.text = 'Scale the selected photo(s) by what percent of their original size?'
v1.add_subview(lb1)

lb2 = ui.Label(frame = (99, 166, 150, 37))
lb2.font = ('<system-bold>', 18)
lb2.flex = 'LRTB'
lb2.alignment = ui.ALIGN_LEFT
lb2.text = 'Keep Metadata:'
v1.add_subview(lb2)

lb3 = ui.Label(frame = (99, 224, 150, 37))
lb3.font = ('<system-bold>', 18)
lb3.flex = 'LRTB'
lb3.alignment = ui.ALIGN_LEFT
lb3.text = 'Geotag Photos:'
v1.add_subview(lb3)

lb4 = ui.Label(frame = (99, 36, 150, 37))
lb4.font = ('<system-bold>', 18)
lb4.flex = 'HLRTB'
lb4.alignment = ui.ALIGN_LEFT
lb4.text = 'Options:'
v1.add_subview(lb4)

lb5 = ui.Label(frame = (99, 107, 150, 37))
lb5.font = ('<system-bold>', 18)
lb5.flex = 'HLRTB'
lb5.alignment = ui.ALIGN_LEFT
lb5.text = 'Photo Dir:'
v1.add_subview(lb5)

# Controls for v2
btn4 = ui.Button(frame = (63, 317, 292, 59))
btn4.font = ('<system-bold>', 15)
btn4.flex = 'HLRTB'
btn4.border_width = 2
btn4.tint_color = 'black'
btn4.background_color = '#7af685'
btn4.action = button_tapped
btn4.title = 'Ok'
btn4.name = 'ok_button'
v2.add_subview(btn4)

tf2 = ui.TextField(frame =(172, 208, 77, 48))
tf2.font = ('<system-bold>', 17)
tf2.flex = 'HLRTB'
tf2.alignment = ui.ALIGN_CENTER
tf2.border_width = 2
tf2.text = '35'
v2.add_subview(tf2)

lb6 = ui.Label(frame = (82, 57, 264, 89))
lb6.font = ('<system-bold>', 18)
lb6.flex = 'LRTB'
lb6.alignment = ui.ALIGN_CENTER
lb6.number_of_lines = 0
lb6.text = 'Enter desired percent of selected photo(s) original size to scale for a Dropbox copy.'
v2.add_subview(lb6)

def main(assets, keep_meta, geo_tag, dest_dir, size):
  minumum_size = True
  resizePercent = 0
  # This is time in seconds to allow for dropbox to process each photo.  Older iOS devices will require more time.
  upload_pause = 3

  if size == 'fifty':
    scale = float(50) / 100
  elif size == 'custom': 
    scale = tf2
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
      console.hud_alert('Script Cancelled')
      sys.exit()
  
  elif size == 'none':
    scale = 1

  # Disable idle timer to cover working with a large batch of photos
  console.set_idle_timer_disabled(True)

  start = time.clock()

  # Create an instance of Dropbox client
  drop_client = get_client()

  for asset in assets:
    print('\nProcessing photo...')
    '''
    Get date & time photo was created on YOUR iOS device.
    Note that in some cases the creation date may not be the
    date the photo was taken (ie you got it via text, email, Facebook, etc), but rather the date the photo was saved
    to the camera roll on your device.
    '''
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
    if orientation in ('1', '3'):
      img = img.resize((new_w, new_h),Image.ANTIALIAS)
      # Occasionally metadata will say the photo orientation is 1 even though the width is less than the height of photo. 
      oriented = 'portrait' if new_w < new_h else 'landscape'
    # Portrait
    elif orientation in ('6', '8'):
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
    assets = photos.pick_asset(all_assets, title = 'Select Desired Photos', multi=True)
  else:
    console.hud_alert('Camera roll is empty')
    sys.exit()
    
  # Were any photos selected?
  try:
    count = len(assets)
  except TypeError:
    console.hud_alert('No photos selected')
    sys.exit()

  # Default pic sizes
  fifty = custom = none = ok = False
  
  # Display ui locked in portrait orientation and wait till user makes choices or quits.
  v1.present(orientations = ['portrait'])
  v1.wait_modal()
  
  # Get user option choices for keeping metadata and geo_tagging photos
  meta = sw1.value
  geo = sw2.value
  dest_dir = tf1.text

  # Go with default if textbox is blank
  if len(dest_dir) == 0:
    dest_dir = '/Photos'
  # Check syntax
  elif dest_dir[:1] != '/':
    dest_dir = '/' + dest_dir

  # If user pressed the close button then close any loaded views and cancel script
  if fifty == custom == none == False:
    v2.close()
    console.hud_alert('Script cancelled')
    sys.exit()
    
  # Otherwise store resizing choice in a variable to pass to main()
  elif fifty:
    size = 'fifty'
  elif custom:
    size = 'custom'
  elif none:
    size = 'none'

  main(assets, meta, geo, dest_dir, size)
