# coding: utf-8
'''
写真から顔を検出して笑い男のマークを上書きする pythonista extention
'''
import appex
import console
import photos
import Image
from objc_util import *

[CIFilter, CIImage, CIContext, CIDetector, CIVector, NSValue] = list(map(ObjCClass,
                                                                         ['CIFilter', 'CIImage', 'CIContext',
                                                                          'CIDetector','CIVector', 'NSValue']))

def load_ci_image(img_filename):
	data = NSData.dataWithContentsOfFile_(img_filename)
	if not data:
		raise IOError('Could not read file')
	ci_img = CIImage.imageWithData_(data)
	return ci_img
	
def load_mask_ci_image():
	#img = Image.open('emj:Smiling_2')
	#img = Image.open('laughingman.png')
	
	if img:
		img.save('.mask.png')
		return load_ci_image('.mask.png')
		
def find_faces(ci_img):
	'''顔を検出して顔領域のリストを返す'''
	d = CIDetector.detectorOfType_context_options_('CIDetectorTypeFace', None, {'CIDetectorAccuracy': 'CIDetectorAccuracyHigh'})
	rects = d.featuresInImage_(ci_img)
	if rects.count() == 0:
		return None
	return rects
	
def mask_faces(ci_img, faces):
	face_num = 1
	for r in faces:
		b = r.bounds()
		w=b.size.width
		h=b.size.height
		rt=CGPoint(b.origin.x+w,b.origin.y+h)
		rb=CGPoint(b.origin.x+w,b.origin.y)
		lt=CGPoint(b.origin.x,b.origin.y+h)
		lb=CGPoint(b.origin.x,b.origin.y)
		
		print('face: %d' % face_num)
		face_num += 1
		
		mask_img = load_ci_image('laughingman.png')
		rect = mask_img.extent()
		filter1 = CIFilter.filterWithName_('CIAffineTransform')
		filter1.setDefaults()
		filter1.setValue_forKey_(mask_img, 'inputImage')
		scale = b.size.width/rect.size.width
		trans = CGAffineTransform(scale, 0, 0, scale, b.origin.x, b.origin.y)
		filter1.setValue_forKey_(NSValue.valueWithCGAffineTransform(trans), 'inputTransform')
		mask_img = filter1.valueForKey_('outputImage')
		
		filter = CIFilter.filterWithName_('CISourceOverCompositing')
		filter.setDefaults()
		filter.setValue_forKey_(ci_img, 'inputBackgroundImage')
		filter.setValue_forKey_(mask_img, 'inputImage')
		ci_img = filter.valueForKey_('outputImage')
	return ci_img
	
def view_ci_image(ci_img):
	filename = write_output(ci_img)
	console.show_image(filename)
	
def write_output(out_ci_img, filename='.output.jpg'):
	ctx = CIContext.contextWithOptions_(None)
	cg_img = ctx.createCGImage_fromRect_(out_ci_img, out_ci_img.extent())
	ui_img = UIImage.imageWithCGImage_(cg_img)
	c.CGImageRelease.argtypes = [c_void_p]
	c.CGImageRelease.restype = None
	c.CGImageRelease(cg_img)
	c.UIImageJPEGRepresentation.argtypes = [c_void_p, CGFloat]
	c.UIImageJPEGRepresentation.restype = c_void_p
	data = ObjCInstance(c.UIImageJPEGRepresentation(ui_img.ptr, 0.75))
	data.writeToFile_atomically_(filename, True)
	return filename
	
def pick_photo(filename='.temp.jpg'):
	img = photos.pick_image()
	if img:
		img.save(filename)
		return filename
		
def main():
	if appex.is_running_extension():
		images = appex.get_attachments('public.jpeg')
	else:
		print('Pick a photo to mask.')
		images = [pick_photo()]
		
	print(images)
	
	if not images:
		print('No input image found')
		return
	ci_img = load_ci_image(images[0])
	faces = find_faces(ci_img)
	if not faces:
		print('Error: No faces found in the photo.')
		return
	out_img = mask_faces(ci_img, faces)
	out_file = write_output(out_img)
	console.clear()
	console.show_image(out_file)
	console.alert('Tweet this image?')
	
	
if __name__ == '__main__':
	main()

