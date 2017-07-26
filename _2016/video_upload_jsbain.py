# https://gist.github.com/jsbain/de01d929d3477a4c8e7ae9517d5b3d70

from objc_util import *
import photos
import time

assets=photos.get_assets(media_type='video')

options=ObjCClass('PHVideoRequestOptions').new()
options.version=1	#PHVideoRequestOptionsVersionOriginal, use 0 for edited versions.
image_manager=ObjCClass('PHImageManager').defaultManager()

handled_assets=[]

def handleAsset(_obj,asset, audioMix, info):
	A=ObjCInstance(asset)
	'''I am just appending to handled_assets to process later'''
	handled_assets.append(A)
	'''
	# alternatively, handle inside handleAsset.  maybe need a threading.Lock here to ensure you are not sending storbinaries in parallel
	with open(str(A.resolvedURL().resourceSpecifier()),'rb') as fp:
		fro.storbinary(......)
	'''
	
handlerblock=ObjCBlock(handleAsset, argtypes=[c_void_p,]*4)

for A in assets:
	#these are PHAssets
	image_manager.requestAVAssetForVideo(A, 
						options=options, 
						resultHandler=handlerblock)
						
while len(handled_assets) < len(assets):
	'''wait for the asynchronous process to complete'''
	time.sleep(1)

just_testing=True
''' for testing purposes, just read the file in chunks, to ensure no memory leaks, etc.  set to false, and set up your ftp client to actually upload'''

for A in handled_assets:
	with open(str(A.resolvedURL().resourceSpecifier()),'rb') as fp:
		if just_testing:
			while fp.read(16*1024):
				pass
			print(fp.tell(), 'bytes read')
		else:
			filename=str(A.URL()).split('/')[-1]
			ftp.storbinary('STOR '+filename,fp)
			

	



