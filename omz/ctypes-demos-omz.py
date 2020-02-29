# coding: utf-8

# https://forum.omz-software.com/topic/1588/beta-build-160008/33

# Some experimental `ctypes` demos for Pythonista on iOS

from __future__ import print_function
from ctypes import c_void_p, c_char_p, c_double, c_float, cdll, util
import os

# Load Objective-C runtime:
objc = cdll.LoadLibrary(util.find_library('objc'))
objc.sel_getName.restype = c_char_p
objc.sel_getName.argtypes = [c_void_p]
objc.sel_registerName.restype = c_void_p
objc.sel_registerName.argtypes = [c_char_p]
objc.objc_getClass.argtypes = [c_char_p]
objc.objc_getClass.restype = c_void_p

# Some helper methods:
def obj_to_str(obj):
    objc.objc_msgSend.argtypes = [c_void_p, c_void_p]
    objc.objc_msgSend.restype = c_void_p
    desc = objc.objc_msgSend(obj, objc.sel_registerName('description'))
    objc.objc_msgSend.argtypes = [c_void_p, c_void_p]
    objc.objc_msgSend.restype = c_char_p
    return objc.objc_msgSend(desc, objc.sel_registerName('UTF8String'))

def msg(obj, restype, sel, argtypes=None, *args):
    if argtypes is None:
        argtypes = []
    objc.objc_msgSend.argtypes =  [c_void_p, c_void_p] + argtypes
    objc.objc_msgSend.restype = restype
    res = objc.objc_msgSend(obj, objc.sel_registerName(sel), *args)
    return res

def cls(cls_name):
    return objc.objc_getClass(cls_name)

def nsstr(s):
    return msg(cls('NSString'), c_void_p, 'stringWithUTF8String:', [c_char_p], s)

# Demo:

def print_ipod_title():
    MPMusicPlayerController = cls('MPMusicPlayerController')
    player = msg(MPMusicPlayerController, c_void_p, 'iPodMusicPlayer')
    item = msg(player, c_void_p, 'nowPlayingItem')
    if item:
        artist = msg(item, c_void_p, 'valueForProperty:', [c_void_p], nsstr('artist'))
        title = msg(item, c_void_p, 'valueForProperty:', [c_void_p], nsstr('title'))
        print('Now Playing: %s -- %s' % (obj_to_str(artist), obj_to_str (title)))
    else:
        print('iPod not playing')

def set_screen_brightness(value):
    UIScreen = cls('UIScreen')
    main_screen = msg(UIScreen, c_void_p, 'mainScreen')
    msg(main_screen, None, 'setBrightness:', [c_float], value)

def save_video(video_file):
    uikit = cdll.LoadLibrary(util.find_library('UIKit'))
    save_func = uikit.UISaveVideoAtPathToSavedPhotosAlbum
    save_func.argtypes = [c_void_p] * 4
    save_func(nsstr(os.path.abspath(video_file)), None, None, None)

def download_and_save_video():
    # Download a short sample file from Apple:
    # http://support.apple.com/en-us/HT201549
    if not os.path.exists('sample_mpeg4.mp4'):
        print('Downloading test video...')
        import urllib, zipfile
        urllib.urlretrieve('http://a1408.g.akamai.net/5/1408/1388/2005110405/1a1a1ad948be278cff2d96046ad90768d848b41947aa1986/sample_mpeg4.mp4.zip', 'temp.zip')
        zipfile.ZipFile('temp.zip').extractall()
        os.remove('temp.zip')
    print('Saving video...')
    save_video('sample_mpeg4.mp4')
    print('Done')

if __name__ == '__main__':
    from time import sleep
    print('Printing currently playing music (iPod/Music app only)...')
    print_ipod_title()
    sleep(1)
    print('Downloading a video, and saving it to the camera roll...')
    download_and_save_video()
    print('Making screen very bright...')
    sleep(1)
    set_screen_brightness(1.0)
    print('...very dark...')
    sleep(1)
    set_screen_brightness(0.0)
    print('...and something in-between.')
    sleep(1)
    set_screen_brightness(0.5)

