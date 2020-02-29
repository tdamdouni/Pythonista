# https://github.com/jiayiliu/c3d

"""
Controller for circle drawer
"""
from __future__ import print_function

__author__ = 'jiayiliu'


from c3plot import *

#!TODO generator for circles
#!TODO model to link orientation

class C3control():
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.elev = 30
        self.azim = 45
        self.ax.view_init(elev=self.elev, azim=self.azim)
        self.fig.canvas.mpl_connect('key_press_event', self.rotate)
        test2(self.ax)
        plt.show()

    def rotate(self, event):
        if event.key == "left":
            print(event.key)
            self.azim += 1
        elif event.key == "right":
            self.azim -= 1
        elif event.key == "up":
            self.elev -= 1
        elif event.key == "down":
            self.elev += 1
        self.ax.view_init(elev=self.elev, azim=self.azim)
        self.fig.canvas.draw()

if __name__ == "__main__":
    a= C3control()
