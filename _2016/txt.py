# https://gist.github.com/zacbir/11d71e79b4559c77394b06b9ec6ec3d7

from datetime import datetime

from quartz import quartz

width = height = 1024.0

color_space = quartz.CGColorSpaceCreateWithName(quartz.kCGColorSpaceSRGB)
ctx = quartz.CGBitmapContextCreate(None, width, height, 8, width * 4, color_space, quartz.kCGImageAlphaPremultipliedLast)

quartz.CGContextSetRGBFillColor(ctx, 1, 0, 0, 1)

r = quartz.CGRectMake(0, 0, width, height)
quartz.CGContextAddRect(ctx, r)
quartz.CGContextDrawPath(ctx, quartz.kCGPathFillStroke)

image = quartz.CGBitmapContextCreateImage(ctx)

filename = "{}.png".format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
url = quartz.CFURLCreateFromFileSystemRepresentation(None, filename, len(filename), False)
dest = quartz.CGImageDestinationCreateWithURL(url, 'public.png', 1, None)
quartz.CGImageDestinationAddImage(dest, image, None)
quartz.CGImageDestinationFinalize(dest)
