# coding: utf-8

# https://forum.omz-software.com/topic/3016/access-to-apple-standard-language-dictionaries/11

from objc_util import ObjCClass, UIApplication, CGSize, on_main_thread,ObjCInstance
import sys
import ui

UIReferenceLibraryViewController = ObjCClass('UIReferenceLibraryViewController')

back= ui.View()
back.background_color='gray'
back.name = 'Dictionary'
back.present('full_screen',hide_title_bar=False)

input = 'word'
referenceViewController = UIReferenceLibraryViewController.alloc().initWithTerm_(input)

ObjCInstance(back).addSubview_(referenceViewController)

# ObjCInstance(back).addSubview_(referenceViewController.view())

rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
tabVC = rootVC.detailViewController()

referenceViewController.setTitle_('Definition: {0}{1}{0}'.format('\'', input))
referenceViewController.setPreferredContentSize_(CGSize(540, 540))
referenceViewController.setModalPresentationStyle_(2)
#tabVC.addTabWithViewController_(referenceViewController)
tabVC.presentViewController_animated_completion_(referenceViewController, True, None)

