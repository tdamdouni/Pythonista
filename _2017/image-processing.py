# https://forum.omz-software.com/topic/4504/image-processing-using-objc

from PIL import Image, ImageOps, ImageFilter, ImageChops
import photos, clipboard, webbrowser

imo=clipboard.get_image(idx=0)

if not imo.mode == 'RGB':
	img=imo.convert('RGB')

	im1=img.filter(ImageFilter.MaxFilter(size=9))

	im2=ImageChops.subtract(im1,img)

	im3=ImageOps.invert(im2)

	im4=im3.filter(ImageFilter.SHARPEN)

	im5=ImageOps.autocontrast(im4,cutoff=1)

clipboard.set_image(im5,jpeg_quality=1.0)
webbrowser.open('workflow://')
