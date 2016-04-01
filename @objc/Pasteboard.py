# coding: utf-8

# https://forum.omz-software.com/topic/2319/multi-frame-gifs-to-clipboard-or-photos/13

from objc_util import *

UIPasteboard=ObjCClass('UIPasteboard')
pb=UIPasteboard.generalPasteboard()

#method 1: works but creates a .png:
#imgdata = UIImage.imageWithContentsOfFile_('test.gif')
#pb.setImage_(imgdata)

# method 2: does not work. pasteboard is empty
imgdata = NSData.dataWithContentsOfFile_('test.gif')
pb.setData_forPasteboardType_(imgdata, ns('kUTTypeGIF'))

# @omz: Method 2 should work if you use 'com.compuserve.gif' (the UTI for GIF images) instead of 'kUTTypeGIF'. The latter is the name of a constant/macro, it would get replaced by the preprocessor if you were writing actual Objective-C code. I've tested this with an animated GIF, and was able to paste it in an email.