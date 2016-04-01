## Demonstrates some techniques for working with "faces", and
## shows how to build a height field (a common feature request)
## with it.
## David Scherer July 2001
## Revised January 2010 by Bruce Sherwood to use faces.smooth() function
##   introduced with VPython 5.2
## Revised March 2010 by Bruce Sherwood to use faces.make_normals() and
## faces.make_twosided() functions introduced with VPython 5.3

from visual import *

class Model:
    def __init__(self):
        self.frame = frame()
        self.model = faces(frame=self.frame, color=color.cyan)
        self.vertices = []

    def FacetedTriangle(self, v1, v2, v3, color=color.white):
        """Add a triangle to the model"""
        for v in (v1,v2,v3):
            self.vertices.append(v)

    def FacetedPolygon(self, *v):
        """Appends a planar polygon of any number of vertices to the model"""
        for t in range(len(v)-2):
            self.FacetedTriangle( v[0], v[t+1], v[t+2] )

    def DrawNormals(self, scale):
        pos = self.model.pos
        normal = self.model.normal
        for i in range(len(pos)):
            arrow(pos=pos[i], axis=normal[i]*scale)

class Mesh (Model):
    def __init__(self, xvalues, yvalues, zvalues):
        Model.__init__(self)

        points = zeros( xvalues.shape + (3,), float )
        points[...,0] = xvalues
        points[...,1] = yvalues
        points[...,2] = zvalues

        for i in range(zvalues.shape[0]-1):
            for j in range(zvalues.shape[1]-1):
                self.FacetedPolygon( points[i,j], points[i,j+1],
                                     points[i+1,j+1], points[i+1,j] )
                
        self.model.pos = self.vertices
        self.model.make_normals()
        self.model.smooth()
        self.model.make_twosided()

## Graph a function of two variables (a height field)
x = arange(-1,1,2./20)
y = arange(-1,1,2./20)

z = zeros( (len(x),len(y)), float )
x,y = x[:,None]+z, y+z

m = Mesh( x, (sin(x*pi)+sin(y*pi))*0.2, y )
##m.DrawNormals(0.05)

