# coding: utf-8

# https://forum.omz-software.com/topic/2576/interesting-method-name

[x for x in dir(ObjCClass('PAMoveFilesViewController').alloc().init()) if x.startswith('at')]

