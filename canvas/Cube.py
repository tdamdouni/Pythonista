# coding: utf-8

# Based loosely on http://codentronix.com/2011/05/12/rotating-3d-cube-using-python-and-pygame/

from __future__ import print_function
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
    print(str((x/360.0)*100.0)[:5]+'%')

writeGif('cube.gif', images, 0.01)
