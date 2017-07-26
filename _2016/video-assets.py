# https://forum.omz-software.com/topic/3728/having-trouble-writing-a-video-file-to-local-storage-ends-up-corrupted/2

from objc_util import *
import threading
import photos

def get_video_path(asset):
	if asset.media_type != 'video':
		raise ValueError('Not a video asset')
	PHImageManager = ObjCClass('PHImageManager')
	mgr = PHImageManager.defaultManager()
	e = threading.Event()
	result = {}
	def handler_func(_cmd, _av_asset, _audio_mix, _info):
		av_asset = ObjCInstance(_av_asset)
		if av_asset.isKindOfClass_(ObjCClass('AVURLAsset')):
			asset_url = av_asset.URL()
			asset_path = str(asset_url.path())
			result['path'] = asset_path
		e.set()
	ph_asset = ObjCInstance(asset)
	handler = ObjCBlock(handler_func, restype=None, argtypes=[c_void_p]*4)
	mgr.requestAVAssetForVideo_options_resultHandler_(ph_asset, None, handler)
	e.wait()
	return result.get('path', None)
	
# Demo: Pick a video asset from the library, then copy the video file to Pythonista, and show a QuickLook preview...
if __name__ == '__main__':
	asset = photos.pick_asset()
	video_path = get_video_path(asset)
	if video_path:
		import shutil, console, os
		shutil.copy(video_path, 'video.m4v')
		console.quicklook(os.path.abspath('video.m4v'))
	else:
		print('Could not get video file path')

