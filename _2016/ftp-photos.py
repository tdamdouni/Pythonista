# https://forum.omz-software.com/topic/3299/get-filenames-for-photos-from-camera-roll/13

import photos
from objc_util import *
from ftplib import FTP
import console
p = photos.pick_asset(assets=photos.get_assets(media_type='video'))
file_name = str(ObjCInstance(p).valueForKey_('filename'))
b = p.get_image_data()
try:
	ftp = FTP('Server') #connect
	ftp.encoding = 'utf-8'
	ftp.login('User','pwd')
	ftp.storbinary('STOR '+file_name,b)
	ftp.close()
except Exception as e:
	console.alert('Error ',str(e),'ok',hide_cancel_button=True)
loc_file = open(file_name,mode='wb')
loc_file.write(b.getvalue())
loc_file.close()
