# coding: utf-8
import numpy as np
from PIL import Image, ImageDraw
from images2gif import writeGif
from math import sin,cos


W,H = 1024,1024
duration = 2
ncircles = 20 # Number of circles

def polar2cart(r,theta):
    x = r*cos(theta)
    y = r*sin(theta)
    return x, y

def make_frame(t):

    im = Image.new('RGB', (W,H), (0,0,0))
    
    surface = ImageDraw.Draw(im)

    for i in range(ncircles):
        angle = 2*np.pi*(1.0*i/ncircles+t/duration)
        center = W*( 0.5 + polar2cart(0.1,angle)[0]), W*( 0.5 + polar2cart(0.1,angle)[1])
        r = W*(1.0-1.0*i/ncircles)
        bbox = (center[0]-r, center[1]-r, center[0]+r, center[1]+r)
        surface.ellipse(bbox, fill= (i%2*255,i%2*255,i%2*255))
        
    del surface
    return im.resize((256,256), Image.ANTIALIAS)

images = []
for x in range(50):
    images.append(make_frame(x/25.0))

writeGif('tunnelswirl.gif',images,0.005)
