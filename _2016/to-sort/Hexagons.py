# coding: utf-8

from __future__ import print_function
import colorsys, console
import numpy as np
from images2gif import writeGif
from PIL import Image, ImageDraw

sin, cos, pi = np.sin, np.cos, np.pi
W,H = 1024,1024
NFACES = 5 #Number of faces on the polygon
R = 0.3 #Radius of polygon
NSQUARES = 100 # Number of squares
DURATION = 1

def polar_polygon(nfaces,radius, npoints):
    """ Returns the (x,y) coordinates of n points regularly spaced
    along a regular polygon of `nfaces` faces and given radius.
    """
    theta=np.linspace(0,2*np.pi,npoints)[:-1]
    n = nfaces
    r= cos( pi/n )/cos((theta%(2*pi/n))-pi/n)
    d = np.cumsum(np.sqrt(((r[1:]-r[:-1])**2)))
    d = [0]+list(d/d.max())
    return zip(radius*r, theta, d)

def polar2cart(r,theta):
    x = r*cos(theta)
    y = r*sin(theta)
    return x, y

def squarecoords(sidelength, center, angle):
    cx, cy = center
    radius = sidelength/2
    corners = [(cx-radius,cy-radius), (cx+radius,cy-radius), (cx+radius,cy+radius), (cx-radius,cy+radius)]

    def rotate(point, angle, center=(0, 0)):
        theta = angle*(np.pi/180.0)
        translated = point[0]-center[0] , point[1]-center[1]
        rotated = (translated[0]*cos(theta)-translated[1]*sin(theta),translated[0]*sin(theta)+translated[1]*cos(theta))
        newcoords = (round(rotated[0]+center[0], 1),round(rotated[1]+center[1], 1))
        return newcoords
    newcorners = []
    for x in corners:
        newcorners.append(rotate(x,angle,center))
    
    return tuple([tuple([int(x) for x in y]) for y in newcorners])

def half(t, side="left"):
    points = polar_polygon(NFACES, R, NSQUARES)
    ipoint = 0 if side=="left" else NSQUARES/2
    points = (points[ipoint:]+points[:ipoint])[::-1]

    i = Image.new('RGB', (W, H), (0,0,0))
    surface = ImageDraw.Draw(i)

    for (r, th, d) in points:
        center = W*(0.5+polar2cart(r,th)[0]),W*(0.5+polar2cart(r,th)[1])
        #angle = -(np.pi*d + t*np.pi/DURATION)*50
        angle = -(t*180)
        
        color= colorsys.hls_to_rgb((2*d+t/DURATION)%1,.5,.5)
        color = tuple([int(x*255) for x in color])
        coords = squarecoords(0.17*W, center, angle)
        surface.polygon(coords, color, outline=(255,255,255))
    im = np.asarray(i)
    return (im[:,:W/2] if (side=="left") else im[:,W/2:])

def make_frame(t):
    lefthalf = half(t,"left")
    righthalf = half(t,"right")
    return Image.fromarray(np.hstack((lefthalf, righthalf)))

images = []
for x in range(100):
    images.append(make_frame(x/100.0).resize((512,512), Image.ANTIALIAS))
    console.clear()
    print(str(x+1)+'%')

console.clear()
print('Writing gif...')
writeGif("pentagon.gif", images, duration=0.01)
