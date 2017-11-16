# https://gist.github.com/omz/61373e17a7a450f2eb9f2b2b43ca2b5f

# https://forum.omz-software.com/topic/4504/image-processing-using-objc/6

'''
This module provides a Python wrapper around CIImage and CIFilter for using CoreImage filters from Pythonista more easily.

How to use:

1) Create a CImage object. The constructor accepts either a file path, a ui.Image, PIL.Image.Image, or photos.Asset object. Example:

>>> # From a photo:
>>> img = CImage(photos.pick_asset())
>>> # From a ui.Image:
>>> img2 = CImage(ui.Image.named('test:Peppers'))
>>> # From a file:
>>> img3 = CImage('MyImage.jpg')

2) Apply a filter using the CImage object's filter() method. The list of available filters and their parameter names can be found here:
https://developer.apple.com/library/content/documentation/GraphicsImaging/Reference/CoreImageFilterReference/index.html

The result is another CImage object that can be filtered again, to build a filter chain. When all filters have been applied, you can use the show() method to display the result in the console, or save_jpeg()/save_png() to save it to a file.

Filter parameters are passed to the filter() method as keyword arguments. If a parameter name begins with "input" (almost all do), that prefix can be left out for better readability (e.g. inputSaturation=... becomes just saturation=...).

The filter reference will tell you which type each parameter should be. This can be translated to Python as follows:

NSNumber:		int or float
CIVector:		tuple of numbers (int or float), often x/y coordinates
CIImage:		CImage object
CIColor:		Either a color string (e.g. '#ff000', 'red'), a tuple with 3 or 4 numbers (rgb[a]) in the range 0.0-1.0, or a number (grayscale value)
NSString:		str
NSData:			bytes or str (the latter will be utf-8-encoded)

Example:

>>> img = CImage(photos.pick_asset())
>>> img2 = img.filter('CIColorControls', saturation=2.0, contrast=1.5)
>>> img3 = img2.filter('CIGaussianBlur', radius=10)
>>> img3.show()

The inputImage parameter is always set automatically. If a filter doesn't have an inputImage parameter (e.g. a gradient or barcode generator), you can just create an empty CImage and "filter" that. Example:

>>> empty = CImage()
>>> qrcode = empty.filter('CIQRCodeGenerator', message='Hello World')
>>> qrcode.show()
'''

from objc_util import *
import photos
import os
import ui
import PIL.Image
import tempfile
import numbers

class CImage(object):
	def __init__(self, img_or_path=None):
		CIImage = ObjCClass('CIImage')
		if img_or_path is None:
			self.ci_img = CIImage.emptyImage()
			return
		if isinstance(img_or_path, ObjCInstance):
			if img_or_path.isKindOfClass_(CIImage):
				self.ci_img = img_or_path
				return
		if isinstance(img_or_path, PIL.Image.Image):
			buffer = io.BytesIO()
			img_or_path.save(buffer, 'PNG')
			img_or_path = ui.Image.from_data(buffer)
		if isinstance(img_or_path, photos.Asset):
			img_or_path = img_or_path.get_ui_image()
		if isinstance(img_or_path, ui.Image):
			self.ci_img = CIImage.imageWithCGImage_(ObjCInstance(img_or_path).CGImage())
		elif isinstance(img_or_path, str):
			file_url = nsurl(os.path.abspath(img_or_path))
			self.ci_img = CIImage.imageWithContentsOfURL_(file_url)
		else:
			raise TypeError('unsupported type for initializing CImage')

	def filter(self, name, **params):
		CIFilter = ObjCClass('CIFilter')
		CIVector = ObjCClass('CIVector')
		CIColor = ObjCClass('CIColor')
		filter = CIFilter.filterWithName_(name)
		if not filter:
			raise ValueError('Invalid filter name')
		filter.setDefaults()
		input_keys = [str(k) for k in filter.inputKeys()]
		attrs = filter.attributes()
		input_key_types = {
			str(k): str(attrs[k]['CIAttributeClass'])
			for k in input_keys
		}
		supported_types = {
			'CIImage': CImage,
			'CIVector': tuple,
			'CIColor': (tuple, numbers.Number, str),
			'NSNumber': numbers.Number,
			'NSData': (bytes, str),
			'NSString': str
		}
		if 'inputImage' in input_keys:
			filter.setValue_forKey_(self.ci_img, 'inputImage')
		for key, value in params.items():
			if key not in input_keys:
				key = 'input' + key[0].upper() + key[1:]
			if key not in input_keys:
				raise ValueError('"%s" is not a valid parameter for %s' % (key, name))
			param_type = input_key_types[key]
			if param_type not in supported_types:
				raise TypeError('Parameters of type %s are not supported' % param_type)
			expected_type = supported_types[param_type]
			type_matches = isinstance(value, expected_type)
			if not type_matches:
				raise TypeError(
					'Incorrect type for %s parameter (expected %s, got %s)' %
					(key, expected_type, type(value))
				)
			if param_type == 'CIColor':
				if isinstance(value, numbers.Number):
					value = (value, value, value, 1.0)
				elif isinstance(value, str):
					value = ui.parse_color(value)
				if not all(isinstance(n, numbers.Number) for n in value):
					raise TypeError('All color components must be numbers')
				if len(value) == 3:
					ci_color = CIColor.colorWithRed_green_blue_(*value)
				elif len(value) == 4:
					ci_color = CIColor.colorWithRed_green_blue_alpha_(*value)
				else:
					raise TypeError('Color must be a tuple with 3 or 4 RGB(A) values')
				filter.setValue_forKey_(ci_color, key)
			elif param_type == 'CIImage':
				filter.setValue_forKey_(value.ci_img, key)
			elif param_type == 'CIVector':
				arr = (CGFloat * len(value))(*value)
				vector = CIVector.vectorWithValues_count_(arr, len(value))
				filter.setValue_forKey_(vector, key)
			elif param_type == 'NSData' and isinstance(value, str):
				filter.setValue_forKey_(value.encode('utf-8'), key)
			else:
				filter.setValue_forKey_(value, key)
		out_img = filter.valueForKey_('outputImage')
		return CImage(out_img)

	def _uiimage_rep(self):
		# Internal helper method for save_jpeg and save_png
		ctx = ObjCClass('CIContext').context()
		extent = self.ci_img.extent()
		m = ctx.outputImageMaximumSize()
		if extent.size.width > m.width or extent.size.height > m.height:
			# This is probably an infinite image, render *something*...
			extent = CGRect(CGPoint(0, 0), CGSize(1024, 1024))
		cg_img = ctx.createCGImage_fromRect_(self.ci_img, extent)
		ui_img = UIImage.imageWithCGImage_(cg_img)
		c.CGImageRelease.argtypes = [c_void_p]
		c.CGImageRelease.restype = None
		c.CGImageRelease(cg_img)
		return ui_img

	def save_jpeg(self, filename='output.jpg', quality=1.0):
		ui_img = self._uiimage_rep()
		c.UIImageJPEGRepresentation.argtypes = [c_void_p, CGFloat]
		c.UIImageJPEGRepresentation.restype = c_void_p
		data = ObjCInstance(c.UIImageJPEGRepresentation(ui_img.ptr, quality))
		filename = os.path.abspath(filename)
		return data.writeToFile_atomically_(filename, True)

	def save_png(self, filename='output.png'):
		ui_img = self._uiimage_rep()
		c.UIImagePNGRepresentation.argtypes = [c_void_p]
		c.UIImagePNGRepresentation.restype = c_void_p
		data = ObjCInstance(c.UIImagePNGRepresentation(ui_img.ptr))
		filename = os.path.abspath(filename)
		return data.writeToFile_atomically_(filename, True)

	def show(self):
		temp_path = os.path.join(tempfile.gettempdir(), 'cimage_show.png')
		saved = self.save_png(temp_path)
		if saved:
			ui.Image.named(temp_path).show()
		else:
			raise ValueError('Image could not be saved (may be empty)')


def main():
	img = CImage(ui.Image.named('test:Mandrill'))
	img = img.filter('CITwirlDistortion', center=(256, 256), radius=150)
	img = img.filter('CICMYKHalftone')
	img.show()

if __name__ == '__main__':
	main()
