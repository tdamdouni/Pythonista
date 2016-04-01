import Image, ImageOps, ImageFilter
from Image import BILINEAR
from math import sqrt, sin, cos, atan2
import dialogs
import photos

def sketch(img):
	edge_img = img.filter(ImageFilter.CONTOUR)
	return ImageOps.grayscale(edge_img)

def emboss(img):
	edge_img = img.filter(ImageFilter.CONTOUR)
	return ImageOps.grayscale(edge_img)

def color_tiles(img):
	size = img.size
	small_img = img.resize((size[0]/2, size[1]/2), BILINEAR)
	bw_img = small_img.convert('1', dither=False)
	gray_img = bw_img.convert('L')
	result = Image.new('RGB', size)
	tile1 = ImageOps.colorize(gray_img, 'green', 'red') 
	tile2 = ImageOps.colorize(gray_img, 'purple', 'yellow')
	tile3 = ImageOps.colorize(gray_img, 'yellow', 'brown')
	tile4 = ImageOps.colorize(gray_img, 'red', 'cyan')
	result.paste(tile1, (0, 0))
	result.paste(tile2, (size[0]/2, 0))
	result.paste(tile3, (0, size[1]/2))
	result.paste(tile4, (size[0]/2, size[1]/2))
	return result

def main():
	effect = dialogs.alert('Select Effect', '', 'Sketch', 'Emboss', 'Color Tiles')
	i = dialogs.alert('Image', '', 'Demo Image', 'Select from Photos')
	if i == 1:
		img = Image.open('test:Lenna')
	else:
		img = photos.pick_image()
	if effect == 1:
		sketch(img).show()
	elif effect == 2:
		emboss(img).show()
	else:
		color_tiles(img).show()
	print 'Tip: You can tap and hold the image to save it to your photo library.'

if __name__ == '__main__':
	main()