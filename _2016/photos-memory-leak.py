# https://gist.github.com/jsbain/c26545118d79b505ebf6425bedebad71

# https://forum.omz-software.com/topic/3844/photos-asset-get_image_data-is-there-a-memory-leak/4

import photos,sys,ui,io
from objc_util import *
import sys,os
sys.path+=os.path.expanduser('~')
from objc_hacks.memstatus import _get_taskinfo

import gc
from PIL import Image

options = ObjCClass('PHImageRequestOptions').defaultOptionsAllowingPlaceholder()
options.deliveryMode = 1 #high quality
options.synchronous = True

imageManager = ObjCClass('PHImageManager').defaultManager()


def handleImage(_obj,result,infodict):
	try:
		img=ObjCInstance(result)
		d=ObjCInstance(infodict)
		#print(d)
		filename=handleImage.filename
		#print(filename)
		# Do something with the bytes
		#. Example: convert to PIL
		bIO=io.BytesIO(uiimage_to_png(img))
		i=Image.open(bIO)
		#print(i)
	finally:
		# Cleanup, avoid reference cycle in objcinstances
		img._cached_methods.clear()
		img=[]
		d._cached_methods.clear()
		d=[]
		bIO.close()
		i=[]
		bIO=[]
handleImage.filename='' #just to avoid global
B=ObjCBlock(handleImage,argtypes=[c_void_p,c_void_p,c_void_p],restype=None)


def process_images(thumbnail=True):
	all_assets = photos.get_assets()
	photo_count = len(all_assets)
	photo_index = 0
	while photo_index<photo_count:
		ass = all_assets[photo_index]
		a=ObjCInstance(ass)
		if thumbnail:
			requested_size=CGSize(160,160)
		else:
			requested_size=a.imageSize() # for fullsize
		handleImage.filename=str(a.filename())
		imageManager.requestImageForAsset(ass,
		targetSize=requested_size,
		contentMode=1,
		options=options,
		resultHandler=B)
		a._cached_methods.clear()
		a=[]
		ass=[]
		photo_index += 1
		#print(_get_taskinfo().resident_size/1024/1024)
		
process_images()
print(_get_taskinfo().resident_size/1024/1024)

gc.collect(2)

