# coding: utf-8

# https://forum.omz-software.com/topic/2970/objc_util-uitextview-and-attributed-text

import objc_util
import sys

@on_main_thread
def test_001():
    red = UIColor.redColor()
    font = ObjCClass('UIFont').systemFontOfSize_(30.)
    mystring = ObjCClass('NSMutableAttributedString').alloc() 
    teststring = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tincidunt facilisis dapibus.'
    mystring.initWithString_(teststring)
    #d_red = NSDictionary.alloc().initWithObjectsAndKeys_([red, 'NSForegroundColorAttributeName', None]) # crash
    d_red = NSDictionary.alloc().initWithObjects_forKeys_((red,), ('NSForegroundColorAttributeName',)) 
    mystring.setAttributes_range_(d_red, NSRange(10, 15))
    tv = ui.TextView()
    tvc = ObjCInstance(tv)
    
    #tvc.setAttributedText_(mystring)
    # the following line works just fine (why?)
    tvc.attributedText = mystring 
    tvc.setFont_(font) # ok
    tv.present()
