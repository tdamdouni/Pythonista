# coding: utf-8

# https://forum.omz-software.com/topic/2460/mac-address-using-uuid-getnode

#from uuid import getnode
#print getnode()

# You can get your device's name:
import objc_util
str(objc_util.ObjCClass('UIDevice').currentDevice().name())

# Which mean's you need to give your devices unique names, but that doesn't seem too objectionable.

# You could also use

str(objc_util.ObjCClass('UIDevice').currentDevice().identifierForVendor().UUIDString())

# Which I haven't tested through reboots, but this is supposed to be the Apple approved way of getting unique id's. It does not survive remove/reinstalls apparantly. Of course, you could generate your own random uuid, and store it in the keychain -- either way you need to know this in advance before you can deploy anything. Storing your own would make you robust to changes in identifierForVendor across ios versions.
