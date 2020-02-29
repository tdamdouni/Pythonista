#!python2

# https://gist.github.com/omz/0d5a709bbb4186d1f45f2af14c65b110

# Experimental photo picker using the Photos framework via objc_util. Compared to the photos module, this has the advantage of showing all photos, including iCloud photo library. Not very well tested!

from __future__ import print_function
from objc_util import *
import threading
from io import BytesIO
from PIL import Image
import sys
import ui
import ctypes

NSBundle.bundleWithPath_('/System/Library/Frameworks/Photos.framework').load()
PHAsset = ObjCClass('PHAsset')
PHImageManager = ObjCClass('PHImageManager')
PHImageRequestOptions = ObjCClass('PHImageRequestOptions')
mgr = PHImageManager.defaultManager()

def nsdata2str(data):
	return ctypes.string_at(data.bytes(), data.length())
	
class Asset (object):
	def __init__(self, asset_obj):
		self._asset = asset_obj
		
	def __repr__(self):
		return repr(self._asset)
		
	def fetch_data(self):
		'''Return a tuple of (UTI, data) for the asset. Both are strings, the UTI indicates the file type (e.g. 'public.jpeg').'''
		e = threading.Event()
		result = {}
		def handler(_cmd, _data, _uti, orientation, _info):
			if _data:
				result['data'] = nsdata2str(ObjCInstance(_data))
				result['uti'] = str(ObjCInstance(_uti))
				result['orientation'] = orientation
				result['info'] = ObjCInstance(_info)
			e.set()
		handler_block = ObjCBlock(handler, restype=None, argtypes=[c_void_p, c_void_p, c_void_p, NSInteger, c_void_p])
		options = PHImageRequestOptions.new().autorelease()
		options.networkAccessAllowed = True
		options.synchronous = True
		mgr.requestImageDataForAsset_options_resultHandler_(self._asset, options, handler_block)
		e.wait()
		return result
		
	def fetch_ui_thumbnail(self):
		a = self._asset
		options = PHImageRequestOptions.new().autorelease()
		options.networkAccessAllowed = True
		options.synchronous = True
		target_size = CGSize(80, 80)
		result = {}
		e = threading.Event()
		def handler(_cmd, _result, _info):
			result['image'] = ObjCInstance(_result)
			e.set()
		handler_block = ObjCBlock(handler, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])
		mgr.requestImageForAsset_targetSize_contentMode_options_resultHandler_( a, target_size, 0, options, handler_block)
		e.wait()
		return result['image']
		
	def fetch_image(self):
		'''Return the asset as a decoded PIL Image object.'''
		info = self.fetch_data()
		img_data = info['data']
		orientation = info['orientation']
		b = BytesIO(img_data)
		img = Image.open(b)
		# NOTE: Mirrored orientations are not supported here.
		orientations = {1: 180, 2: 90, 3: -90}
		rotation = orientations.get(orientation, 0)
		if rotation != 0:
			img = img.rotate(rotation)
		return img
		
UICollectionView = ObjCClass('UICollectionView')
UICollectionViewFlowLayout = ObjCClass('UICollectionViewFlowLayout')
UICollectionViewCell = ObjCClass('UICollectionViewCell')
UIImageView = ObjCClass('UIImageView')
UIColor = ObjCClass('UIColor')

def collectionView_numberOfItemsInSection_(_self, _cmd, _cv, _sec):
	ds = ObjCInstance(_self)
	return len(ds.assets)
collectionView_numberOfItemsInSection_.encoding = 'q32@0:8@16q24'

def collectionView_cellForItemAtIndexPath_(_self, _cmd, _cv, _ip):
	ds = ObjCInstance(_self)
	ip = ObjCInstance(_ip)
	cv = ObjCInstance(_cv)
	asset = ds.assets[ip.item()]
	thumb = asset.fetch_ui_thumbnail()
	cell = cv.dequeueReusableCellWithReuseIdentifier_forIndexPath_('Cell', ip)
	iv = cell.viewWithTag_(123)
	if not iv:
		iv_frame = cell.bounds()
		iv = UIImageView.alloc().initWithFrame_(iv_frame).autorelease()
		iv.setTag_(123)
		iv.setContentMode_(2)
		iv.setClipsToBounds_(True)
		iv.setAutoresizingMask_(18)
		cell.addSubview_(iv)
	iv.setImage_(thumb)
	return cell.ptr
collectionView_cellForItemAtIndexPath_.encoding = '@32@0:8@16@24'

def collectionView_didSelectItemAtIndexPath_(_self, _cmd, _cv, _ip):
	ds = ObjCInstance(_self)
	ds.selected_asset_index = ObjCInstance(_ip).item()
	ds.asset_collection_view.close()
collectionView_didSelectItemAtIndexPath_.encoding = 'v32@0:8@16@24'

methods = [collectionView_numberOfItemsInSection_, collectionView_cellForItemAtIndexPath_, collectionView_didSelectItemAtIndexPath_]
DataSource = create_objc_class('DataSource', methods=methods, protocols=['UICollectionViewDelegateFlowLayout', 'UICollectionViewDataSource', 'UICollectionViewDelegate'])

class AssetCollectionView (ui.View):
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		layout = UICollectionViewFlowLayout.alloc().init().autorelease()
		layout.itemSize = CGSize(80, 80)
		layout.sectionInset = UIEdgeInsets(8, 8, 8, 8)
		frame = ((0, 0), (self.bounds.width, self.bounds.height))
		cv = UICollectionView.alloc().initWithFrame_collectionViewLayout_(frame, layout)
		cv.backgroundColor = UIColor.whiteColor()
		cv.registerClass_forCellWithReuseIdentifier_(UICollectionViewCell, 'Cell')
		ds = DataSource.alloc().init().autorelease()
		res = PHAsset.fetchAssetsWithMediaType_options_(1, None)
		ds.assets = [Asset(res.objectAtIndex_(i)) for i in xrange(res.count())]
		ds.asset_collection_view = self
		self.data_source = ds
		cv.dataSource = ds
		cv.delegate = ds
		cv.setAlwaysBounceVertical_(True)
		cv.setAutoresizingMask_(18)
		ObjCInstance(self._objc_ptr).addSubview_(cv)
		
def pick_asset():
	av = AssetCollectionView(frame=(0, 0, 540, 576))
	av.name = 'All Photos'
	av.present('sheet')
	av.wait_modal()
	if hasattr(av.data_source, 'selected_asset_index'):
		asset = av.data_source.assets[av.data_source.selected_asset_index]
		return asset
	else:
		return None
		
# Demo:
def main():
	asset = pick_asset()
	if asset:
		img = asset.fetch_image()
		img.show()
	else:
		print('No image picked')
		
if __name__ == '__main__':
	main()

