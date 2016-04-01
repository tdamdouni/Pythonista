# coding: utf-8
import numpy as np
from PIL import Image, ImageDraw
from images2gif import writeGif
from math import sin,cos
import ui
import io

W,H = 128,128
duration = 2
ncircles = 20 # Number of circles

def polar2cart(r,theta):
    x = r*cos(theta)
    y = r*sin(theta)
    return x, y

def ui2pil(ui_img):
    png_data = ui_img.to_png()
    return Image.open(io.BytesIO(png_data))

def make_frame(t):
    with ui.ImageContext(W, H, 1) as ctx:
        for i in range(ncircles):
            angle = 2*np.pi*(1.0*i/ncircles+t/duration)
            center = W*( 0.5 + polar2cart(0.1,angle)[0]), W*( 0.5 + polar2cart(0.1,angle)[1])
            r = W*(1.0-1.0*i/ncircles)
            ui.set_color((i%2, i%2, i%2))
            ui.Path.oval(center[0]-r, center[1]-r, r*2, r*2).fill()
        return ui2pil(ctx.get_image())

#images = []
#for x in range(200):
#    images.append(make_frame(x/25.0))
#images = [make_frame(x/25.0) for x in xrange(200)]  # ;-)
images.append(make_frame(x/25.0).convert('RGB'))
writeGif('tunnelswirl.gif',images,0.005)
