# coding: utf-8

# https://forum.omz-software.com/topic/3728/having-trouble-writing-a-video-file-to-local-storage-ends-up-corrupted

import vimeo
import photos
from io import BytesIO
from objc_util import ObjCInstance

client = vimeo.VimeoClient(token='my_api_token')

video_asset = photos.pick_asset()
video_data = video_asset.get_image_data()
video_bytes = video_data.getvalue()
filename = str(ObjCInstance(video_asset).filename())

with open(filename, 'wb') as video:
	video.write(video_bytes)
video.close()

video_uri = client.upload(filename)

