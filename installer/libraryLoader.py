from __future__ import print_function
# https://gist.github.com/Cethric/bab622410267ed4dc054

# coding: utf-8
import os
import sys
import ctypes
from ctypes import util
from objc_util import *

def loadLibrary(library):
    bundle = ObjCClass("NSBundle").bundleWithPath_(library)
    print(bundle)
    preflightError = ctypes.c_void_p()
    preflight = bundle.preflightAndReturnError_(ctypes.byref(preflightError))
    
    if not preflight:
        error = ObjCInstance(preflightError)
        userinfo = error.userInfo()
        print('ERROR', error.code())
        print('Failed to run preflight on the Framework: %s' % userinfo['NSBundlePath'])
        print(error.localizedDescription())
        print(error.localizedRecoverySuggestion())
        print(userinfo['NSDebugDescription'])
        return
    
    loadError = ctypes.c_void_p()
    loaded = bundle.loadAndReturnError_(ctypes.byref(loadError))
    if not loaded:
        error = ObjCInstance(preflightError)
        userinfo = error.userInfo()
        print('ERROR', error.code())
        print('Failed to load the Framework: %s' % userinfo['NSBundlePath'])
        print(error.localizedDescription())
        print(error.localizedRecoverySuggestion())
        return
    
    print('Loaded Library:', bundle.bundlePath())
    print('Version:', bundle.versionNumber())
    print('Executable:', bundle.executablePath())
    print('Identifier:', bundle.bundleIdentifier())
    principalClass = bundle.principalClass()
    
    if principalClass is None:
        print('So close. But sadly this library has no principalClass')
        return
    principalClass = ObjCInstance(principalClass)
    return principalClass
        
if __name__ == '__main__':
    pui = loadLibrary('/System/Library/Frameworks/PhotosUI.framework')
    print(pui)