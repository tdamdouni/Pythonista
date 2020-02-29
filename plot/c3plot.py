# https://github.com/jiayiliu/c3d

"""
Plot circle in 3D
"""
from __future__ import print_function

__author__ = 'jiayiliu'

from math import pi, cos, sin
import numpy as np
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import axes3d


def rotate_x(theta):
    """
    create the rotation matrix around x-axis
    """
    c = cos(theta)
    s = sin(theta)
    return np.matrix([[1,0,0],[0,c,-s],[0,s,c]])

def rotate_y(theta):
    """
    create the rotation matrix around y-axis
    """
    c = cos(theta)
    s = sin(theta)
    return np.matrix([[c,0,s],[0,1,0],[-s,0,c]])

def rotate_z(theta):
    """
    create the rotation matrix around z-axis
    """
    c = cos(theta)
    s = sin(theta)
    return np.matrix([[c,-s,0],[s,c,0],[0,0,1]])


def draw_circle(ax, x0, phi, r0, **args):
    """
    draw a circle in 3D space

    :param ax: axis to plot
    :param x0: 3D position [x,y,z]
    :param phi: direction of circle
    :param r0: radius
    :param args: other parameters to control plotting
    """
    # assign initial matrix of circle on x-y plane
    theta = np.linspace(0, 2*pi, num=int(r0/0.01))
    xyz = np.zeros((len(theta),3))
    xyz[:,0] = np.cos(theta)*r0
    xyz[:,1] = np.sin(theta)*r0
    # rotate around
    #rotation_matrix = rotate_x(phi[0])*rotate_y(phi[1])*rotate_z(phi[2])
    xyz = np.matrix(xyz) * rotate_x(phi[0])*rotate_y(phi[1])*rotate_z(phi[2])
    # convert back to array
    xyz = np.squeeze(np.asarray(xyz)) + x0
    ax.plot(xyz[:,0], xyz[:,1], xyz[:,2], **args)
    return xyz


def draw_circle_direction(ax, x0, phi, length=1):
    """
    draw the direction of circle in 3D space

    :param ax: axis to plot
    :param x0: 3D position [x,y,z]
    :param phi: direction of circle
    """
    di = np.matrix([[0,0,-length],[0,0,length]])
    di = di*rotate_x(phi[0])*rotate_y(phi[1])*rotate_z(phi[2])
    di = np.squeeze(np.asarray(di)) + x0
    ax.plot(di[:,0],di[:,1],di[:,2])
    return di


def test1(ax):
    rr = draw_circle(ax, [1,3,1], [0,1.,1.], 1)
    p = draw_circle_direction(ax,[1,3,1],[0,1.,1.])
    print(np.sum((p[0]-rr)**2,axis=1))
    print(np.sum((p[1]-rr)**2,axis=1))


def test2(ax):
    for i in range(10):
        draw_circle(ax,np.random.random(3), np.random.random(3), 1)

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    test2(ax)
    plt.show()
