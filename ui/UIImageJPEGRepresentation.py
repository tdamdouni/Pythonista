from __future__ import print_function
# https://forum.omz-software.com/topic/2327/uiimagejpegrepresentation

# coding: utf-8
import os
import Image
import ui

def captureNow(sender):
    print("Capture Screen")
    layer = v.layer()
    UIGraphicsBeginImageContext(layer.bounds().size)
    layer.renderInContext_(UIGraphicsGetCurrentContext())
    # v.drawViewHierarchyInRect_afterScreenUpdates_(v.bounds(), True)
    image = ObjCInstance(UIGraphicsGetImageFromCurrentImageContext())
    UIGraphicsEndImageContext()
    
    vt = ui.View()
    vt.width = 800
    vt.height = 600
    
    UIImageView = ObjCClass('UIImageView')
    iview = UIImageView.alloc().initWithImage_(image)
    iview.setFrame_(ObjCInstance(vt).bounds())
    
    print(iview)
    
    ObjCInstance(vt).addSubview_(iview)
    vt.present('sheet')
    
    UIImageJPEGRepresentation(image, 1.0).writeToFile_atomically_('test.jpg', True)
def UIImageJPEGRepresentation(image, compressionQuality):
    func = c.UIImageJPEGRepresentation
    func.argtypes = [ctypes.c_void_p, ctypes.c_float]
    func.restype = ctypes.c_void_p
    return ObjCInstance(func(image.ptr, compressionQuality))