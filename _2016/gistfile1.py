# https://gist.github.com/jsbain/99303488cf6af6d7ef8b9b43a46ca414

from datetime import datetime
from objc_util import c, CGRect, nsurl,ns,ObjCInstance, ObjCClass,NSURL
from quartz import quartz
from ctypes import c_void_p, c_int, c_double, c_float, c_size_t,c_bool, c_char_p, sizeof
import os
if sizeof(c_size_t)==8:
	CFFloat=c_double
else:
	CFFloat=c_float
width = height = 1024	#this needs to be an integer, no decimal
kCGColorSpaceSRGB=ObjCInstance(c_void_p.in_dll(quartz,'kCGColorSpaceSRGB'))
kCGImageAlphaPremultipliedLast=1
kCGPathFillStroke=3

#these are needed because argtypes are not all voids
quartz.CGImageDestinationCreateWithURL.argtypes=[c_void_p,c_void_p,c_int,c_void_p]
quartz.CGContextSetRGBFillColor.argtypes=[c_void_p, CFFloat, CFFloat, CFFloat, CFFloat]
quartz.CGColorSpaceCreateWithName.argtypes=[c_void_p]
quartz.CFURLCreateFromFileSystemRepresentation.argtypes=[c_void_p,c_char_p,c_size_t,c_bool]

#for some rewson this one fails.
color_space = quartz.CGColorSpaceCreateWithName(kCGColorSpaceSRGB)
if not color_space:
	color_space=quartz.CGColorSpaceCreateDeviceRGB()
	print('falling back to devicergb colorspace')

ctx = quartz.CGBitmapContextCreate(None, width, height, 8, width * 4, 
							color_space, kCGImageAlphaPremultipliedLast)
if not ctx:
	raise Exception('Context not created')

quartz.CGContextSetRGBFillColor(ctx, 1., 0., 0., 1.)

#use CGRect to make rects.
r = CGRect((0, 0), (width, height))
quartz.CGContextAddRect(ctx, r)
quartz.CGContextDrawPath(ctx, kCGPathFillStroke)

image = quartz.CGBitmapContextCreateImage(ctx)
if not image:
	raise Exception('Image not created')

#for easy viewing, use uiimage
uiim=ObjCClass('UIImage').imageWithCGImage_(ObjCInstance(image))
import ui
i=ui.ImageView()
ObjCInstance(i).image=uiim
i.present('sheet')

# abspaths are needed
filename = os.path.abspath("{}.png".format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S')))

#simpler alternative:
#url=NSURL.fileURLWithPath_(filename)
url = quartz.CFURLCreateFromFileSystemRepresentation(None, filename.encode('latin1'), len(filename), False)
if not url:
	raise Exception('could not create url')
	
dest = quartz.CGImageDestinationCreateWithURL(url, ns('public.png'), 1, None)
if not dest:
	raise Exception('could not create dest')
quartz.CGImageDestinationAddImage(dest, image, None)
quartz.CGImageDestinationFinalize(dest)
if not os.path.exists(filename):
	raise Exception('file not created')

#clean up
quartz.CFRelease(dest)
quartz.CGImageRelease(image)
quartz.CGContextRelease(ctx)
quartz.CGColorSpaceRelease(color_space)

