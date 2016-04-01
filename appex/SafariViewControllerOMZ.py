# https://forum.omz-software.com/topic/2271/beta-suggestion-safariviewcontroller

# coding: utf-8

from objc_util import *

SFSafariViewController = ObjCClass('SFSafariViewController')

@on_main_thread
def open_in_safari_vc(url, tint_color=None):
    vc = SFSafariViewController.alloc().initWithURL_(nsurl(url))
    if tint_color is not None:
        vc.view().tintColor = tint_color
    app = UIApplication.sharedApplication()
    root_vc = app.keyWindow().rootViewController()
    root_vc.presentViewController_animated_completion_(vc, True, None)
    vc.release()

if __name__ == '__main__':
    open_in_safari_vc('http://apple.com', UIColor.blueColor())