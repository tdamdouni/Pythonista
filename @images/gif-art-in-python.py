https://forum.omz-software.com/topic/2052/gif-art-in-python/13

import numpy as np
import gizeh
import moviepy.editor as mpy

W,H = 128,128
duration = 2
ncircles = 20 # Number of circles

def make_frame(t):

    surface = gizeh.Surface(W,H)

    for i in range(ncircles):
        angle = 2*np.pi*(1.0*i/ncircles+t/duration)
        center = W*( 0.5+ gizeh.polar2cart(0.1,angle))
        circle = gizeh.circle(r= W*(1.0-1.0*i/ncircles),
                              xy= center, fill= (i%2,i%2,i%2))
        circle.draw(surface)

    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif("circles.gif",fps=15, opt="OptimizePlus", fuzz=10)

#==============================

# coding: utf-8
import numpy as np
from PIL import Image, ImageDraw
from images2gif import writeGif
from math import sin,cos


W,H = 128,128
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
    return im

images = []
for x in range(200):
    images.append(make_frame(x/25.0))

writeGif('tunnelswirl.gif',images,0.005)

#==============================

images = [make_frame(x/25.0) for x in xrange(200)]  # ;-)

#==============================

images.append(make_frame(x/25.0).convert('RGB'))

#==============================

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

#==============================

# coding: utf-8

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
    print str(x+1)+'%'

console.clear()
print 'Writing gif...'
writeGif("pentagon.gif", images, duration=0.01)

#==============================

# coding: utf-8

import math
from operator import itemgetter

import console
from images2gif import writeGif
from PIL import Image, ImageDraw



W, H = (1024, 1024)
class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)


class Cube:
    def __init__(self, win_width = 640, win_height = 480):
        
        self.vertices = [
        Point3D(-1,1,-1),
        Point3D(1,1,-1),
        Point3D(1,-1,-1),
        Point3D(-1,-1,-1),
        Point3D(-1,1,1),
        Point3D(1,1,1),
        Point3D(1,-1,1),
        Point3D(-1,-1,1)
        ]
        
        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
        
        # Define colors for each face
        self.colors = [
                        '#FFEC94',
                        '#FFAEAE',
                        '#404040',
                        '#B0E57C',
                        '#B4D8E7',
                        '#7BC8A4'
                        ]
    
    def make_frame(self, angle):
        # It will hold transformed vertices.
        t = []
        
        screen = Image.new('RGB',(W, H), (255,255,255))
        draw = ImageDraw.Draw(screen)
        
        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(angle).rotateY(angle).rotateZ(angle)
            # Transform the point from 3D to 2D
            
            #if angle <= 180:
            #   p = r.project(W, H, 256, 3+(angle/90.0))
            #else:
            #   p = r.project(W, H, 256, 5-((angle-180)/90.0))
            p = r.project(W, H, 256, 3)
            # Put the point in the list of transformed vertices
            t.append(p)
            
        # Calculate the average Z values of each face.
        avg_z = []
        i = 0
        for f in self.faces:
            z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
            avg_z.append([i,z])
            i = i + 1
        
        # Draw the faces using the Painter's algorithm:
        # Distant faces are drawn before the closer ones.
        for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
            face_index = tmp[0]
            f = self.faces[face_index]
            pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
            (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
            (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
            (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
            draw.polygon(pointlist, fill=self.colors[face_index])
            
        return screen.resize((512,512), Image.ANTIALIAS)

c = Cube()
images = []
for x in range(0,360,5):
    images.append(c.make_frame(x))
    console.clear()
    print str((x/360.0)*100.0)[:5]+'%'

writeGif('cube.gif', images, 0.01)

#==============================

Duration = 1

#==============================

Duration = 1.0

#==============================

# coding: utf-8
from images2gif import writeGif
from PIL import Image, ImageDraw, ImageChops

import console



W, H = 1024,1024
RESOLUTION = 5
FG, BG = '#ffbb00', '#009bff'

#FG, BG = '#000000', '#ffffff'


def drange(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    else:
        return([])

def irange(start, increments):
    mylist = [start]
    for i in increments:
        mylist.append(mylist[-1]+i)
    return mylist

    
class Rect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.right = left + width
        self.top = top
        self.bottom = top+height

        self.centerx = left + (width/2)
        self.centery = top + (height/2)

        self.width = width
        self.height = height

        self.bbox = (left, top), (self.right, self.bottom)

def drawSierpinski(surf, rect, fgcolor=FG, bgcolor=BG, level=6, topshade=True):
    try:
        rect.left
    except AttributeError:
        left, top, width, height = rect
        rect = Rect(left, top, width, height)

    if level == 0:
        return

    quarterWidth = (rect.width/4)+rect.left
    threeQuarterWidth = (rect.width/4*3)+rect.left

    topRect = Rect(quarterWidth, rect.top, (rect.width / 2), (rect.height / 2))
    leftRect = Rect(rect.left, rect.centery, (rect.width/2), (rect.height/2))
    rightRect = Rect(rect.centerx, rect.centery, (rect.width / 2), (rect.height / 2))

    #Shade topleft
    if topshade:
        surf.rectangle((rect.left, rect.top, rect.centerx, rect.bottom), fill=bgcolor)
    #outer triangle
    surf.polygon([(rect.centerx,rect.top),(rect.left,rect.bottom),(rect.right,rect.bottom)],fgcolor)
    #inner upside-down triangle
    surf.polygon([(quarterWidth,rect.centery),(rect.centerx,rect.bottom),(threeQuarterWidth, rect.centery)],bgcolor)

    #do recursive calls
    drawSierpinski(surf, topRect, fgcolor, bgcolor, level-1, topshade)
    drawSierpinski(surf, leftRect, fgcolor, bgcolor, level-1, topshade)
    drawSierpinski(surf, rightRect, fgcolor, bgcolor, level-1, topshade)

    return im

def make_sierpinski(level, topshade=True):
    im = Image.new('RGB', (W, H), (255,255,255))
    surf = ImageDraw.Draw(im)

    drawSierpinski(surf, Rect(0, 0, W, H), FG, BG, level, topshade)
    return im




im = Image.new('RGB', (W, H), (255,255,255))
surf = ImageDraw.Draw(im)

sierpinski1 = make_sierpinski(RESOLUTION)
sierpinski2 = make_sierpinski(RESOLUTION+1)

numbers = [int(n) for n in irange(0, drange(8,4,-0.0475))]

images = []
for x in numbers:
    a = sierpinski1.crop((x, x, W, W)).resize((512, 512), Image.ANTIALIAS)
    b = sierpinski2.crop((x, x, W, W)).resize((512, 512), Image.ANTIALIAS)

    alpha = x / float(W/2)
    images.append(Image.blend(a, b, alpha))
    console.clear()
    print str(alpha*100)+'%'


console.clear()
print 'writing...'

writeGif('sierpinski.gif', images, 2.0/len(images))
