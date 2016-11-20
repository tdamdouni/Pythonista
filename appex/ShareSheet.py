# coding: utf-8

# https://forum.omz-software.com/topic/2915/delete-photos-from-camera-roll

from objc_util import nsurl, UIApplication
app = UIApplication.sharedApplication()
app.openURL_(nsurl('workflow://...'))
