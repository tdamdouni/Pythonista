# https://github.com/jsbain/pythonista_cv

'''
simple cidetector example
'''

from objc_util import *
import ui,scene
CIDetector = ObjCClass('CIDetector')

def rect_to_tuple(r):
	return	[r.origin.x, r.origin.y, r.size.width, r.size.height]
	
	
	
constants=['CIDetectorAccuracy',
				'CIDetectorTypeFace',
				'CIDetectorTypeRectangle',
				'CIDetectorAccuracyLow',
				'CIDetectorAccuracyHigh',
				'CIDetectorAspectRatio',
				'CIDetectorFocalLength',
				'CIDetectorMinFeatureSize'				]
g=globals()
for const in constants:
	g[const]=ObjCInstance(c_void_p.in_dll(c,const))
opts={str(CIDetectorAccuracy):str(CIDetectorAccuracyHigh),
		str(CIDetectorMinFeatureSize):.0}


detector=CIDetector.detectorOfType_context_options_(
								CIDetectorTypeRectangle, 
								#CIDetectorTypeFace,
								None, 
								ns(opts))

img=ui.Image.named('to-detect.JPG')
imgo=ObjCInstance(img)
cii=ObjCClass('CIImage').imageWithCGImage_( ObjCInstance(imgo.CGImage()))
rects=[]
corners=[]
#handle flipped coord sys
feat_opts={str(CIDetectorAspectRatio):0.73}
for r in list(detector.featuresInImage_options_(cii,ns(feat_opts))):
	#okay, should really use topLeft, topRight, etc and perspective xform
	# scale and flip
	#rects.append([2*x/scene.get_screen_scale() for x in rect_to_tuple(r.bounds())])
	corners.append([r.topLeft(),r.topRight(),r.bottomRight(),r.bottomLeft()])
	#rects[-1][1]=img.size.height-rects[-1][1]-rects[-1][3]
	
#display
with ui.ImageContext(img.size.width,img.size.height) as ctx:
	img.draw()
	ui.set_color('red')
	for shape in corners:
		pth=[]
		for pt in shape:
			if not pth:
				pth=ui.Path()		
				pth.move_to(pt.x,img.size.height-pt.y)
			else:
				pth.line_to(pt.x,img.size.height-pt.y)
		pth.close()
		pth.line_width=4
		pth.stroke()
		del pth
	ctx.get_image().show()
del cii
