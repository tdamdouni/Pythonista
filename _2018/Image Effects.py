# Image Effects
# Demonstrates some effects using different modules
# from the Python Imaging Library (PIL).
#
# Tip: You can touch and hold an image in the output
#      to copy it to the clipboard or save it to your
#      camera roll.

import Image, ImageOps, ImageFilter
from Image import BILINEAR
from math import sqrt, sin, cos, atan2

def sketch(img):
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

def twisted(img, strength):
	mesh = []
	m = 16
	w, h = img.size
	for x in xrange(w / m):
		for y in xrange(h / m):
			target_rect = (x * m, y * m, x * m + m, y * m + m)
			quad_points = ((x * m, y * m), (x * m, y * m + m),
		                 (x * m + m, y * m + m), (x * m + m, y * m))
			quad_list = []
			for qx, qy in quad_points:
				dx = w/2 - qx
				dy = h/2 - qy
				d = sqrt(dx**2 + dy**2)
				angle = atan2(dx, dy)
				angle += max((w/2 - d), 0) * strength
				qx = w/2 - sin(angle) * d
				qy = h/2 - cos(angle) * d
				quad_list.append(qx)
				quad_list.append(qy)
			mesh.append((target_rect, quad_list))
	return img.transform(img.size, Image.MESH, mesh, BILINEAR)

def main():
	img = Image.open('Test_Lenna')
	img = img.resize((256, 256), Image.BILINEAR)
	img.show()
	
	sketch(img).show()
	color_tiles(img).show()
	twisted(img, 0.02).show()

if __name__ == '__main__':
	main()
