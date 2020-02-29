from __future__ import print_function
import Image, ImageOps, ImageFilter
from Image import BILINEAR
from math import sqrt, sin, cos, atan2
import photos
import console

def sketch(img):
	edge_img = img.filter(ImageFilter.CONTOUR)
	return ImageOps.grayscale(edge_img)
def main():
	set_img = photos.pick_image()
	photos.save_image(set_img)
	console.clear()
	print("Generating image...")
	console.show_activity()
	sketch(set_img).show()
	console.hide_activity()
	
if __name__ == '__main__':
	main()

