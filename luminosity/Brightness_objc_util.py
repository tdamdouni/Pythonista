# coding: utf-8

# https://forum.omz-software.com/topic/2635/interesting-sample

# Makes a repeating brightness change. Pretty interesting. Try it out!

# NOTE: As you may have seen, I added the time.sleep() function, so it won't screw your battery up too bad. Before I did that, I left the program running for a minute, and I lost about 3%-4% of battery life.

from objc_util import *
from time import sleep

UIScreen = ObjCClass('UIScreen')

screen = UIScreen.mainScreen()

while True:
    if screen.brightness() == 1:
        screen.setBrightness_(0.1)
    else:
        new = float(float(screen.brightness()) + 0.1)
        screen.setBrightness_(new)
    sleep(0.12)
