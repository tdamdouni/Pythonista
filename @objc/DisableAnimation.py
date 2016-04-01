# coding: utf-8

# https://forum.omz-software.com/topic/2497/ios-animations-turn-all-off/6

from objc_util import *
UIView.beginAnimations_(None)
UIView.setAnimationDuration_(0.5)