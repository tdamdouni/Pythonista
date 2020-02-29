from __future__ import print_function
from dropboxlogin import get_client
dropbox_client = get_client()
import keychain
import console
import time
import httplib
from io import BytesIO
import datetime
import webbrowser
import urllib
import clipboard
 
today = datetime.datetime.now()
 
def WorkPic(img):
	titles = console.input_alert('Image Upload', 'Enter your image name below')
	console.show_activity()
	buffer = BytesIO()
	img.save(buffer, 'JPEG', quality=100)
	buffer.seek(0)
	imgname = today.strftime("%Y-%m-%d-at-%H-%M-%S") + '-' + titles + '.jpeg'
	response = dropbox_client.put_file('/MacStories_Team/Photos/Ticci/upload-unedited/' + imgname, buffer)
	console.hide_activity()
	print('Image Uploaded')
	
if __name__ == '__main__':
  import photos
  img = photos.pick_image()
  WorkPic(img)
 
