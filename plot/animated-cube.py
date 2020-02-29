#!/usr/bin/python

# http://pastebin.com/HGzF8n9k

# https://m.youtube.com/watch?v=K5qoS781qOw

#####################################################################
## Cube animation program using python, numpy and matplotlib.  In the
## spirit of old-school demo programs... This progam can teach you one
## thing or two about computer graphics, specially how important it is
## to learn linear algebra.
##
## This also shows a way to create animations using matplotlib. Just
## make a loop that plots each new frame, and save that frame to an
## image. You can then make a film from these images using mplayer or
## whatever. Instead of replotting everything you could just change
## the parameters from the image curves, but in this case it didn't
## seem much of an advantage to do that.
##
## You can see the output on YouTube:
##   http://www.youtube.com/watch?v=K5qoS781qOw
##
## Coded by Nicolau Werneck<nwerneck@gmail.com> in 2011-03-19
##
#####################################################################
 
from __future__ import print_function
from pylab import *
import numpy as np
 
 
#####################################################################
## Produces a rotation matrix from the 3 last components of a
## quaternion.
def quaternion_to_matrix(myx):
    # '''converts from a quaternion representation (last 3 values) to rotation matrix.'''
    xb,xc,xd = myx
 
    xnormsq = xb*xb+xc*xc+xd*xd
 
    if xnormsq < 1:
        ## If inside the unit sphere, these are the components
        ## themselves, and we just have to calculate a to normalize
        ## the quaternion.
        b,c,d = xb,xc,xd
        a = np.sqrt(1-xnormsq)
    else:
        ## Just to work gracefully if we have invalid inputs, we
        ## reflect the vectors outside the unit sphere to the other
        ## side, and use the inverse norm and negative values of a.
        b,c,d = -xb/xnormsq,-xc/xnormsq,-xd/xnormsq
        a = -np.sqrt(1-  1.0/xnormsq  )
        ## This should not be used, it defeats the whole concept that
        ## small (b,c,d) vector norms have small rotation angles. It's
        ## really just to let us work near the borders of the
        ## sphere. Any optimization algorithm should work with
        ## initalizations just inside the spere, and avoid wandering
        ## outside of it.
 
    assert a >= -1
    assert a <= 1
 
    ## Notice we return a transpose matrix, because we work with line-vectors
 
    return np.array([ [(a*a+b*b-c*c-d*d), (2*b*c-2*a*d),     (2*b*d+2*a*c)      ],
                         [(2*b*c+2*a*d),     (a*a-b*b+c*c-d*d), (2*c*d-2*a*b)      ],
                         [(2*b*d-2*a*c),     (2*c*d+2*a*b),     (a*a-b*b-c*c+d*d)] ]  ).T  \
                         / (a*a+b*b+c*c+d*d)
                         
##
#####################################################################
 
 
## Calculate quaternion values using sinusoids over the frame index
## number, and get rotation matrix. Notice that the second parameter
## is the number of frames. That allows us to easily create an
## animation that can be played as a loop.
def crazy_rotation(ind,Nind):
    return quaternion_to_matrix(0.5*sin(pi*2*ind*Nind**-1.*array([1,2,3])))
 
## This function calculate the projected image coordinates form the 3D
## coordinates of the object vertices.
def project(D, vecs):
    return vvs[:,:2]/(vvs[:,[2,2]]-D)
 
## The cube vertices
vs = reshape(mgrid[-1:2:2,-1:2:2,-1:2:2].T, (8,3))
 
## Generate the list of connected vertices
ed=[(j,k)
    for j in range(8)
    for k in range(j,8)
    if sum(abs(vs[j]-vs[k]))==2 ]
 
 
## Camera position
D=-5
 
## Create the figure. figsize needed to set the image sizes at the end...
figure(1, figsize=(6.4,4.8))
 
## create/get the axes object.
ax=subplot(1,1,1)
 
## Set image title.
suptitle('Cube animation')
 
## Number of frames.
Nind=250
 
##
## Now start a loop over the animation frames. The index is used both
## to name the images and to calculate the rotation matrix. You could
## use this index to make some physics stuff...
for ind in range(Nind):
    print(ind)
    ## This is crucial, clears the figure for the new plot.
    ax.clear()
 
    ## Get the rotation matrix for the current frame.
    rotM = crazy_rotation(ind, Nind)
 
    ## Calculate the 3D coordinates of the vertices of the rotated
    ## cube. Just multiply the vectors by the rotation matrix...
    vvs=dot(vs,rotM)
 
    ## Now calculate the image coordinates of the points.
    pt = project(D,vvs)
 
    ## Plot the edges.
    for j,k in ed:
        ax.plot(pt[[j,k],0], pt[[j,k],1], 'g-', lw=3)
 
    ## Plot the vertices.
    ax.plot(pt[:,0], pt[:,1], 'bo')
 
    ## Set axes limits
    ax.axis('equal')
    ax.axis([-0.5,0.5,-0.5,0.5])
 
    ## Save the current frame. We need the dpi (along with the figure
    ## size up there) to set the image size.
    savefig('anim%03d.png'%ind, dpi=100)
